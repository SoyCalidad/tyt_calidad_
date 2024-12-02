# -*- coding: utf-8 -*-

from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class ConfirmationWizard(models.TransientModel):
    _name = 'tyt_recruitment.attendance_confirmation_wizard'
    _description = 'Confirmación'

    campaign_id = fields.Many2one('tyt_recruitment.campaign', string="Campaña relacionada")
    requisition_id = fields.Many2one("tyt_recruitment.requisition")
    attendance_id = fields.Many2one("tyt_recruitment.attendance")

    def action_accept(self):

        # Update attendance if exists, otherwise create a new one for the campaign
        exist_attencance = self.env['tyt_recruitment.attendance'].sudo().search([('campaign_id', '=', self.campaign_id.id)], limit=1)
        current_attendance_id = 0
        if exist_attencance:
            current_attendance_id = exist_attencance.id
        else:
            attendance_date = {
                "campaign_id": self.campaign_id.id,
                "requisition_id": self.requisition_id.id,
                "days": self.campaign_id.days
            }
            spouse = self.env['tyt_recruitment.attendance'].sudo().create(attendance_date)
            current_attendance_id = spouse.id

        # Create prospects to attendance for a campaign
        applicants = self.env['tyt_recruitment.applicant'].sudo().search([
            ('campaign_id', '=', int(self.campaign_id.id)),
            ('status', '=', True),
        ])

        for applicant in applicants:
            # Search a applicant exists for a attendance
            exist_applicant = self.env['tyt_recruitment.attendance_days_of_week'].sudo().search([
                ('applicant_nss', '=', applicant.social_security_number),
                ('attendance_id', '=', current_attendance_id)
            ], limit=1)

            if not exist_applicant:
                new_prospect = {
                    "applicant_id": applicant.id,
                    "attendance_id": current_attendance_id,
                }
                self.env['tyt_recruitment.attendance_days_of_week'].sudo().create(new_prospect)

        return {'type': 'ir.actions.act_window_close'}

    def action_decline(self):
        campaign = self.campaign_id

        return {'type': 'ir.actions.act_window_close'}
    
    def action_open_generate_attendance(self):

        if self.attendance_id.id:
            return {
                'name': 'Vista Form del Registro',
                'type': 'ir.actions.act_window',
                'res_model': 'tyt_recruitment.attendance',
                'view_mode': 'form',
                'res_id': self.attendance_id.id,
                'views': [(False, 'form')], 
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window_close'
            }