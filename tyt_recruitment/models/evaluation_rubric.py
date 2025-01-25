# -*- coding: utf-8 -*-

from odoo import api, models, fields, http
from odoo.http import request
import uuid
from io import BytesIO
import base64
from datetime import datetime
from urllib.parse import quote

import logging
_logger = logging.getLogger(__name__)

class EvaluationRubric(models.Model):
    _name = 'tyt_recruitment.evaluation_rubric'
    _description = 'Rúbrica de evaluación al expositor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'id'

    week = fields.Char(string="Semana", tracking=True)
    date = fields.Char(string="Fecha", tracking=True)
    auditor = fields.Char(string="Auditor", tracking=True)
    coach = fields.Char(string="Entrenador", tracking=True)
    campaign = fields.Char(string="Campaña", tracking=True)
    evaluation = fields.Char(string="Evaluación", tracking=True)
    state = fields.Char(string="Estado", tracking=True)

    attendance_id = fields.Many2one('tyt_recruitment.attendance', string="Capacitación")
    input_evaluation_rubric_ids = fields.One2many('tyt_recruitment.input_evaluation_rubric', 'evaluation_rubric_id', string="Detalles")

    @api.depends('kardex_by_applicant_ids.login')
    def _compute_income(self):
        for record in self:
            record.income = sum(1 for kardex in record.kardex_by_applicant_ids if kardex.login)

    @api.depends('surveys_ids')
    def _compute_survey_counter(self):
        for record in self:
            record.survey_counter = len(record.surveys_ids)
            
    def action_view_signature(self):
        self.view_kardex_certificate = True

class EvaluationRubric(models.Model):
    _name = 'tyt_recruitment.detail_evaluation_rubric'
    _description = 'Pregunta de rúbrica de evaluación al expositor'
    _rec_name = 'id'

    weighing = fields.Integer(string="Ponderación", tracking=True)
    concept = fields.Char(string="Concepto", tracking=True)
    description = fields.Text(string="Descripción", tracking=True)

class EvaluationRubric(models.Model):
    _name = 'tyt_recruitment.input_evaluation_rubric'
    _description = 'Respuesta de rúbrica de evaluación al expositor'
    _rec_name = 'id'  

    compliance = fields.Selection([('yes', 'Sí'), ('no', 'No')], string="Cumple", tracking=True)
    comment = fields.Char(string="Comentario", tracking=True)

    evaluation_rubric_id = fields.Many2one('tyt_recruitment.evaluation_rubric', string="Rúbrica de evaluación")
    detail_evaluation_rubric_id = fields.Many2one('tyt_recruitment.detail_evaluation_rubric', string="Respuesta")

    weighing = fields.Integer(related='detail_evaluation_rubric_id.weighing', string="Ponderación")
    concept = fields.Char(related='detail_evaluation_rubric_id.concept', string="Ponderación")
    description = fields.Text(related='detail_evaluation_rubric_id.description', string="Ponderación")
    
    evalutation_rubric_id = fields.Many2one('tyt_recruitment.evaluation_rubric', string="Componente de rúbrica")