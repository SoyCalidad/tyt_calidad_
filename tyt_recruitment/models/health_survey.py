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

    name = fields.Char(string='Nombre de la encuesta', tracking=True)
    code = fields.Char(string='Código', tracking=True)
    question_ids = fields.One2many("survey.question", 'health_survey_id', string='Preguntass', tracking=True, store=True)

class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    extra_input = fields.Char(string='Título del campo extra')
    extra_input_enabled = fields.Boolean(string='Habilitado')
    is_a_guest_question = fields.Boolean(string='¿Es prospecto?')

    health_survey_id = fields.Many2one('tyt_recruitment.health_survey', string="Pregunta", ondelete='cascade')

class CompleteSurvey(models.Model):
    _name = 'tyt_recruitment.complete_survey'
    _description = 'Encuesta completa'
    _inherit = ['mail.thread']

    state = fields.Selection([('draft', "PorEnviar"),('sent', "Enviado"),], string="Estado", default='draft', tracking=True)
    recruiter_comments = fields.Char(string="Comentarios del reclutador", tracking=True)
    signature_image = fields.Binary(string="Firma del solicitante")
    job_application_id = fields.Many2one("tyt_recruitment.job_application", string="Aplicaicón de trabajo", tracking=True)
    survey_answer_ids = fields.One2many('tyt_recruitment.survey_answer', 'complete_survey_id', string="Respuestas", tracking=True)

class SurveyAnswer(models.Model):
    _name = 'tyt_recruitment.survey_answer'
    _description = 'Respuesta'
    _inherit = ['mail.thread']

    text = fields.Char(string="Respuesta", tracking=True)
    extra_text = fields.Char(string="Campo extra", tracking=True)
    multiple_ids = fields.One2many("tyt_recruitment.multiple_answer", 'survey_answer_id', string='Respuestas multiples', store=True, tracking=True)

    question_id = fields.Many2one("survey.question", string="Pregunta", tracking=True)
    complete_survey_id = fields.Many2one("tyt_recruitment.complete_survey", string="Encuesta completa", ondelete='cascade', tracking=True)

class MultipleAnswer(models.Model):
    _name = 'tyt_recruitment.multiple_answer'
    _description = 'Multiple respuesta'
    _inherit = ['mail.thread']

    text = fields.Char(string="Respuesta detalle", tracking=True)
    survey_answer_id = fields.Many2one('tyt_recruitment.survey_answer', string='Respuesta', ondelete='cascade', tracking=True)