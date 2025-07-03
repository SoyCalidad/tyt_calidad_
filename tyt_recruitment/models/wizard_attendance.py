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
    campaign_ids = fields.Many2many('tyt_recruitment.campaign', string="Campañas relacionadas", required=True)

    def action_accept(self):
        """
        Procesa la aceptación para cada campaña relacionada.
        Actualiza la asistencia existente o crea una nueva para cada campaña.
        Crea prospectos de asistencia para los solicitantes de cada campaña.
        """
        for campaign in self.campaign_ids:
            # 1. Actualizar asistencia si existe, de lo contrario crear una nueva para la campaña actual
            exist_attendance = self.env['tyt_recruitment.attendance'].sudo().search([
                ('campaign_id', '=', campaign.id)
            ], limit=1)

            current_attendance_id = 0
            if exist_attendance:
                current_attendance_id = exist_attendance.id
                _logger.info(f"Asistencia existente encontrada para la campaña {campaign.name} (ID: {campaign.id}). ID de asistencia: {current_attendance_id}")
            else:
                attendance_data = {
                    "campaign_id": campaign.id,
                    "requisition_id": self.requisition_id.id,
                    "center": self.requisition_id.site_id.display_name if self.requisition_id.site_id else False,
                    "days": campaign.days,
                    "week": self.requisition_id.periodo_id.x_name if self.requisition_id.periodo_id else False
                }
                new_attendance = self.env['tyt_recruitment.attendance'].sudo().create(attendance_data)
                current_attendance_id = new_attendance.id
                _logger.info(f"Nueva asistencia creada para la campaña {campaign.name} (ID: {campaign.id}). ID de asistencia: {current_attendance_id}")

            # 2. Crear prospectos de asistencia para los solicitantes de la campaña actual
            applicants = self.env['tyt_recruitment.applicant'].sudo().search([
                ('campaign_id', '=', campaign.id),
                ('status', '=', True),
            ])
            _logger.info(f"Encontrados {len(applicants)} solicitantes activos para la campaña {campaign.name} (ID: {campaign.id}).")

            for applicant in applicants:
                # Solo crear un nuevo prospecto si el solicitante no tiene días de semana asociados
                if not applicant.days_of_week_ids: # Esto es más pythonico que len(applicant.days_of_week_ids) < 1
                    _logger.info(f"Creando prospecto para el solicitante {applicant.name} (ID: {applicant.id}) en la campaña {campaign.name}.")
                    new_data_prospect = {
                        "applicant_id": applicant.id,
                        "attendance_id": current_attendance_id,
                        "right_turn": campaign.turn
                    }
                    new_prospect = self.env['tyt_recruitment.attendance_days_of_week'].sudo().create(new_data_prospect)

                    new_kardex = {
                        "attendance_days_of_week_id": new_prospect.id,
                        "attendance_id": current_attendance_id
                    }
                    self.env['tyt_recruitment.kardex_by_applicant'].sudo().create(new_kardex)
                else:
                    _logger.info(f"El solicitante {applicant.name} (ID: {applicant.id}) ya tiene días de semana asociados. No se creó un nuevo prospecto.")

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