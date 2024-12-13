from odoo import api, fields, models, _


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    employee_number = fields.Char('Número de empleado', compute='_compute_employee_number')

    answer_count = fields.Integer(related='survey_id.answer_count', string='Registrados', store=True)

    state_percentage = fields.Float(compute='_compute_state_percentage', string="State Percentage", store=True)

    @api.depends('survey_id.user_input_ids')
    def _compute_state_percentage(self):
        """
        Calculate the percentage contribution of this record relative to the
        total records in the associated survey.
        """
        print('Computing state percentage')
        for record in self:
            print('Record:', record)
            total_responses = len(record.survey_id.user_input_ids)
            print('Total responses:', total_responses)
            if total_responses > 0:
                print('If -> Setting state percentage')
                # Each record contributes 1/total_responses * 100
                record.state_percentage = (1 / total_responses) * 100
                print('State percentage:', record.state_percentage)
            else:
                record.state_percentage = 0
                print('Else -> State percentage:', record.state_percentage)


    @api.depends('partner_id')
    def _compute_employee_number(self):
        for record in self:
            if record.partner_id.x_studio_empleado:
                record.employee_number = record.partner_id.x_studio_empleado.x_studio_numero
            elif record.partner_id.x_studio_usuario:
                record.employee_number = record.partner_id.x_studio_usuario.x_studio_numero
            else:
                record.employee_number = ''


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    tipo_encuesta_id = fields.Many2one('x_tipo_encuesta', string='Tipo - TYT', related='question_id.tipo_encuesta_id', store=True)
