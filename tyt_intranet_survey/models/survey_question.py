from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    area_encuesta_id = fields.Many2one('x_area_encuesta', string='Area - Typification')
    tipo_encuesta_id = fields.Many2one('x_tipo_encuesta', string='Tipo - Typification')
