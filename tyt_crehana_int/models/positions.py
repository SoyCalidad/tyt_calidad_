# -*- coding: utf-8 -*-
import requests
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Position(models.Model):
    _name = 'tyt_crehana.job_positions'
    _description = 'Posiciones'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    job_id = fields.Many2one('hr.job', string="Puesto de trabajo", default=None, tracking=True)
    level_a = fields.Boolean(string='Nivel A', tracking=True)
    level_b = fields.Boolean(string='Nivel B', tracking=True)
    level_c = fields.Boolean(string='Nivel C', tracking=True)
    level_d = fields.Boolean(string='Nivel D', tracking=True)
    path_to_position_a = fields.Many2one('tyt_crehana.learning_path', string="Ruta de aprendizaje para A", tracking=True)
    path_to_position_b = fields.Many2one('tyt_crehana.learning_path', string="Ruta de aprendizaje para B", tracking=True)
    path_to_position_c = fields.Many2one('tyt_crehana.learning_path', string="Ruta de aprendizaje para C", tracking=True)
    path_to_position_d = fields.Many2one('tyt_crehana.learning_path', string="Ruta de aprendizaje para D", tracking=True)