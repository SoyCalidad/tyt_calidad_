from odoo import models, fields,_

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    custom_description_enabled = fields.Boolean(string='Custom Description', default=False)
    custom_description_line_ids = fields.One2many(
        comodel_name='survey.custom.description.line',
        inverse_name='survey_id',
    )


class SurveyCustomDescriptionLine(models.Model):
    _name = 'survey.custom.description.line'
    _description = 'Survey Custom Description Line'

    survey_id = fields.Many2one('survey.survey', string='Survey', ondelete='cascade')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    login = fields.Text(string='Login', required=True)
    agent = fields.Text(string='Agent', required=True)
    supervisor = fields.Many2one('hr.employee', string='Supervisor', required=True)
    campaign = fields.Many2one('marketing.campaign', string='Campaign', required=True)
    turn = fields.Selection(
        selection=[(' AM', 'AM'), (' PM', 'PM')],
        string='Turno',
        required=True
    )