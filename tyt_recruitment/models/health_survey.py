# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.http import request
import uuid
from io import BytesIO
import base64
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class HealthSurvey(models.Model):
    _name = 'tyt_recruitment.health_survey'
    _description = 'Encuesta de salud'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'iso_base.email_basic']

    name = fields.Char(string='Nombre de la encuesta', tracking=True,)
    code = fields.Char(string='Código', tracking=True)
    question_ids = fields.One2many("survey.question", 'health_survey_id', string='Preguntass', tracking=True, store=True)

    # @api.model
    # def default_get(self, fields_list):
    #     pass

    # @api.model
    # def create(self, vals):
    #     pass

class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    health_survey_id = fields.Many2one('tyt_recruitment.health_survey', string="Pregunta")

class CompleteSurvey(models.Model):
    _name = 'tyt_recruitment.complete_survey'
    _description = 'Encuesta completa'

    state = fields.Selection([('draft', "PorEnviar"),('sent', "Enviado"),], string="Estado", default='draft')
    job_application_id = fields.Many2one("tyt_recruitment.job_application", string="Aplicaicón de trabajo")
    survey_answer_ids = fields.One2many('tyt_recruitment.survey_answer', 'complete_survey_id', string="Respuestas")

class SurveyAnswer(models.Model):
    _name = 'tyt_recruitment.survey_answer'
    _description = 'Respuesta'

    text = fields.Char(string="Respuesta")
    multiple_ids = fields.One2many("tyt_recruitment.multiple_answer", 'survey_answer_id', string='Respuestas multiples', tracking=True, store=True)

    question_id = fields.Many2one("survey.question", string="Pregunta")
    complete_survey_id = fields.Many2one("tyt_recruitment.complete_survey", string="Encuesta completa")

class MultipleAnswer(models.Model):
    _name = 'tyt_recruitment.multiple_answer'
    _description = 'Multiple respuesta'

    text = fields.Char(string="Respuesta detalle")
    survey_answer_id = fields.Many2one('tyt_recruitment.survey_answer', string='Respuesta')