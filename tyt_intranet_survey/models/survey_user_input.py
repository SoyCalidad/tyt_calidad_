from odoo import api, fields, models, _


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    employee_number = fields.Char('Número de empleado', compute='_compute_employee_number')

    @api.depends('partner_id')
    def _compute_employee_number(self):
        for record in self:
            if record.partner_id.x_studio_empleado:
                record.employee_number = record.partner_id.x_studio_empleado.x_studio_numero
            elif record.partner_id.x_studio_usuario:
                record.employee_number = record.partner_id.x_studio_usuario.x_studio_numero
            else:
                record.employee_number = ''
