# -*- coding: utf-8 -*-

from odoo import api, models, fields, http
from odoo.http import request
import uuid
from io import BytesIO
import base64
from datetime import datetime
from urllib.parse import quote

from ..utils.constants import RUBRIC_STATE

import logging
_logger = logging.getLogger(__name__)

class CertificationFeeback(models.Model):
    _name = 'tyt_recruitment.certification_feedback'
    _description = 'Rúbrica de evaluación al expositor'
    _rec_name = 'id'

    date = fields.Date(string="Fecha", tracking=True)

    name = fields.Char(string="Nombre", tracking=True)
    evaluation_average = fields.Float(string="Promedio de Evaluación")

    group = fields.Char(string="Grupo", tracking=True)
    campaign = fields.Char(string="Campaña", tracking=True)
    trainner = fields.Char(string="Entrenador", tracking=True)

    state = fields.Selection(RUBRIC_STATE, string='Estado', default='doing')
   
    attendance_days_of_week_id = fields.Many2one('tyt_recruitment.attendance_days_of_week', string="Detalle de capacitación individual")   

class ComponentFeedback(models.Model):
    _name = 'tyt_recruitment.component_feeback'
    _description = 'Pregunta de rúbrica de evaluación al expositor'
    _rec_name = 'id'

    text = fields.Char(string="Título", tracking=True)