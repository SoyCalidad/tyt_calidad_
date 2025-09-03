import random
from odoo import models, fields, _

class ConfirmationWizard(models.TransientModel):
    _name = 'tyt_recruitment.attendance_confirmation_wizard'
    _description = 'Confirmación'

    campaign_id = fields.Many2one('tyt_recruitment.campaign', string="Campaña relacionada")
    requisition_id = fields.Many2one("tyt_recruitment.requisition")
    attendance_id = fields.Many2one("tyt_recruitment.attendance")
    campaign_ids = fields.Many2many('tyt_recruitment.campaign', string="Campañas relacionadas", required=True, relation='tyt_conf_camp_rel', domain="[('requisition_id', '=', requisition_id)]")
    attendance_groups_sizes = fields.Char(string="Tamaños de Grupos de Asistencia", help="Ingrese tamaños de grupos separados por comas (ej: 2,3,5). Las campañas seleccionadas se distribuirán aleatoriamente en estos grupos.")

    def action_accept(self):
        if not self.campaign_ids:
            return {'type': 'ir.actions.act_window_close'}

        group_sizes_str = self.attendance_groups_sizes or ''
        try:
            group_sizes = [int(s.strip()) for s in group_sizes_str.split(',') if s.strip()]
        except ValueError:
            group_sizes = []

        if not group_sizes:
            group_sizes = [len(self.campaign_ids)]

        available_campaign_ids = list(self.campaign_ids.ids)
        random.shuffle(available_campaign_ids)

        for group_size in group_sizes:
            current_group_campaign_ids = []
            for _ in range(group_size):
                if available_campaign_ids:
                    campaign_id = available_campaign_ids.pop(0)
                    current_group_campaign_ids.append(campaign_id)
                else:
                    break
            
            if not current_group_campaign_ids:
                continue

            current_group_campaigns = self.env['tyt_recruitment.campaign'].sudo().browse(current_group_campaign_ids)

            all_days = []
            for campaign in current_group_campaigns:
                if campaign.days:
                    all_days.extend(campaign.days.split(',') if isinstance(campaign.days, str) else [campaign.days])
            
            unique_days = list(set(all_days))
            combined_days = ','.join(unique_days) if unique_days else False
            
            attendance_data = {
                "campaign_ids": [(6, 0, current_group_campaign_ids)],
                "requisition_id": self.requisition_id.id,
                "center": self.requisition_id.site_id.display_name if self.requisition_id.site_id else False,
                "days": combined_days,
                "week": self.requisition_id.periodo_id.name if self.requisition_id.periodo_id else False
            }
            new_attendance = self.env['tyt_recruitment.attendance'].sudo().create(attendance_data)
            current_attendance_id = new_attendance.id

            all_applicants = self.env['tyt_recruitment.applicant'].sudo().search([
                ('campaign_id', 'in', current_group_campaign_ids),
                ('status', '=', True),
            ])

            for applicant in all_applicants:
                if not applicant.days_of_week_ids:
                    applicant_campaign_turn = applicant.campaign_id.turn if applicant.campaign_id else False
                    
                    new_data_prospect = {
                        "applicant_id": applicant.id,
                        "attendance_id": current_attendance_id,
                        "right_turn": applicant_campaign_turn,
                        "campaign_id": applicant.campaign_id.id
                    }
                    new_prospect = self.env['tyt_recruitment.attendance_days_of_week'].sudo().create(new_data_prospect)

                    new_kardex = {
                        "attendance_days_of_week_id": new_prospect.id,
                        "attendance_id": current_attendance_id
                    }
                    self.env['tyt_recruitment.kardex_by_applicant'].sudo().create(new_kardex)
        
        return {'type': 'ir.actions.act_window_close'}

    def action_decline(self):
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
