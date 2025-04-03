# -*- coding: utf-8 -*-
import requests
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Position(models.Model):
    _name = 'tyt_crehana.job_positions'
    _description = 'Posiciones'

    job_id = fields.Many2one('hr.job', string="Puesto de trabajo", default=None)
    level_a = fields.Boolean(string='Nivel A')
    path_to_position_a = fields.Many2one('tyt_crehana.learning_path', string="Ruta de aprendizaje para A")
    level_b = fields.Boolean(string='Nivel B')
    path_to_position_b = fields.Many2one('tyt_crehana.learning_path', string="Ruta de aprendizaje para B")
    level_c = fields.Boolean(string='Nivel C')
    path_to_position_c = fields.Many2one('tyt_crehana.learning_path', string="Ruta de aprendizaje para C")
    level_d = fields.Boolean(string='Nivel D')
    path_to_position_d = fields.Many2one('tyt_crehana.learning_path', string="Ruta de aprendizaje para D")