# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.http import request
from urllib.parse import quote

import logging

class ProspectSurvey(models.Model):
    _inherit = 'survey.survey'

    success_options = fields.Many2one('tyt_recruitment.success_option_message', String="Opciones de mensaje aprobación")
    failure_options = fields.Many2one('tyt_recruitment.failure_option_message', String="Opciones de mensaje desaprobación")

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