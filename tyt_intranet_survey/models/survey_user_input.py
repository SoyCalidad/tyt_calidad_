from odoo import api, fields, models, _


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    employee_number = fields.Char('Número de empleado', compute='_compute_employee_number')
    answer_count = fields.Integer(related='survey_id.answer_count', string='Registrados', store=True)
    state_percentage = fields.Float(string="State Percentage", store=True)

    @api.depends('partner_id')
    def _compute_employee_number(self):
        for record in self:
            if record.partner_id.empleado:
                record.employee_number = record.partner_id.empleado.numero
            elif record.partner_id.usuario:
                record.employee_number = record.partner_id.usuario.numero
            else:
                record.employee_number = ''


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    tipo_encuesta_id = fields.Many2one('tyt_studio.survey_type', string='Tipo encuesta', related='question_id.tipo_encuesta_id', store=True)
    partner_id = fields.Many2one('res.partner', string='Partner', related='user_input_id.partner_id', store=True)
    employee_number = fields.Char('Número de empleado', related='user_input_id.employee_number', store=True)
    suggested_answer_value = fields.Char('Suggested Answer Value', related='suggested_answer_id.value', store=True, translate=True)
