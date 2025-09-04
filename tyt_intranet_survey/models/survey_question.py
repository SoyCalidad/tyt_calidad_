from odoo import api, fields, models, _


class TYTSurveyQuestionAnswer(models.Model):
    _name = 'tyt.survey.question.answer'
    _description = 'TYT Survey Question Answer'
    _rec_name = 'value'

    value = fields.Char('Suggested Value')
    answer_score = fields.Float('Score')
    active = fields.Boolean('Active', default=True)


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    area_encuesta_id = fields.Many2one('tyt_studio.survey_area', string='Area encuesta')
    tipo_encuesta_id = fields.Many2one('tyt_studio.survey_type', string='Tipo encuesta')
    survey_publish_state = fields.Selection(related='survey_id.publish_state', string='Survey Publish State', store=True)

    @api.onchange('tipo_encuesta_id')
    def _onchange_suggested_answer_ids(self):
        suggested_answers = self.env['tyt.survey.question.answer'].search([])
        for record in self:
            record.suggested_answer_ids = [(5, 0, 0)]
            if record.tipo_encuesta_id:
                record.suggested_answer_ids = [
                    (0, 0, {
                        'value': answer.value,
                        'answer_score': answer.answer_score,
                    }) for answer in suggested_answers
                ]
