# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.http import request
from urllib.parse import quote

import logging

class ProspectSurvey(models.Model):
    _inherit = 'survey.survey'

    success_options = fields.Many2one('tyt_recruitment.success_option_message', String="Opciones de mensaje aprobación")
    failure_options = fields.Many2one('tyt_recruitment.failure_option_message', String="Opciones de mensaje desaprobación")

    end_message_type = fields.Selection(
        [
            ('default', 'Elegir mensaje por defe to'),
            ('custom', 'Mensaje final personalizado'),
        ],
        string="Tipo de mensaje final",
        default='default',
    )

class SuccessOption(models.Model):
    _name = 'tyt_recruitment.success_option_message'
    _description = 'Opciones de mensaje de aprobado'
    _rec_name = 'message'

    message = fields.Char(string='Mensaje de aprobación')
    approved = fields.Boolean(string='Habilitado')

class FailureOption(models.Model):
    _name = 'tyt_recruitment.failure_option_message'
    _description = 'Opciones de mensaje de desaprobado'
    _rec_name = 'message'

    message = fields.Char(string='Mensaje de desaprobación')
    approved = fields.Boolean(string='Habilitado')

class SurveySurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def action_survey_result(self):
        # Llama al método original
        res = super(SurveySurveyUserInput, self).
        ()
        
        for record in self:
            # Accede al cuestionario relacionado
            survey = record.survey_id

            if survey.scoring_success_min:
                # Calcula el puntaje total
                score = record.quizz_score
                if score >= survey.scoring_success_min:
                    # Muestra el mensaje de éxito
                    record.message_post(body=survey.success_options or "¡Felicidades, has aprobado!")
                else:
                    # Muestra el mensaje de fracaso
                    record.message_post(body=survey.failure_options or "Lo sentimos, no has aprobado.")
        
        return res