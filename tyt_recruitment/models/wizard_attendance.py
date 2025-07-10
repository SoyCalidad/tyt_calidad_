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
    campaign_ids = fields.Many2many('tyt_recruitment.campaign', string="Campañas relacionadas", required=True, relation='tyt_conf_camp_rel', domain="[('requisition_id', '=', requisition_id)]")

    def action_accept(self):
        """
        Procesa la aceptación para todas las campañas relacionadas.
        Crea una sola asistencia para todas las campañas.
        Crea prospectos de asistencia para los solicitantes de todas las campañas.
        """
        if not self.campaign_ids:
            return {'type': 'ir.actions.act_window_close'}
        
        # 1. Verificar si existe una asistencia para alguna de las campañas
        exist_attendance = self.env['tyt_recruitment.attendance'].sudo().search([
            ('campaign_id', 'in', self.campaign_ids.ids),
            ('requisition_id', '=', self.requisition_id.id)
        ], limit=1)

        current_attendance_id = 0
        if exist_attendance:
            current_attendance_id = exist_attendance.id
            # Actualizar la asistencia existente para incluir todas las campañas
        else:
            # Crear una nueva asistencia que cubra todas las campañas
            # Combinar los días de todas las campañas
            all_days = []
            for campaign in self.campaign_ids:
                if campaign.days:
                    all_days.extend(campaign.days.split(',') if isinstance(campaign.days, str) else [campaign.days])
            
            # Eliminar duplicados y unir
            unique_days = list(set(all_days))
            combined_days = ','.join(unique_days) if unique_days else False
            
            attendance_data = {
                "campaign_ids": [(6, 0, self.campaign_ids.ids)],
                "requisition_id": self.requisition_id.id,
                "center": self.requisition_id.site_id.display_name if self.requisition_id.site_id else False,
                "days": combined_days,
                "week": self.requisition_id.periodo_id.x_name if self.requisition_id.periodo_id else False
            }
            new_attendance = self.env['tyt_recruitment.attendance'].sudo().create(attendance_data)
            current_attendance_id = new_attendance.id

        # 2. Crear prospectos de asistencia para los solicitantes de todas las campañas
        all_applicants = self.env['tyt_recruitment.applicant'].sudo().search([
            ('campaign_id', 'in', self.campaign_ids.ids),
            ('status', '=', True),
        ])

        for applicant in all_applicants:
            # Solo crear un nuevo prospecto si el solicitante no tiene días de semana asociados
            if not applicant.days_of_week_ids:
                # Obtener el turno de la campaña del solicitante
                applicant_campaign_turn = applicant.campaign_id.turn if applicant.campaign_id else False
                
                new_data_prospect = {
                    "applicant_id": applicant.id,
                    "attendance_id": current_attendance_id,
                    "right_turn": applicant_campaign_turn
                }
                new_prospect = self.env['tyt_recruitment.attendance_days_of_week'].sudo().create(new_data_prospect)

                new_kardex = {
                    "attendance_days_of_week_id": new_prospect.id,
                    "attendance_id": current_attendance_id
                }
                self.env['tyt_recruitment.kardex_by_applicant'].sudo().create(new_kardex)
            else:
                _logger.info(f"El solicitante (ID: {applicant.id}) ya tiene días de semana asociados. No se creó un nuevo prospecto.")

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