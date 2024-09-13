# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Process(models.Model):
    _inherit = 'mgmt.process'

    documentarycontrol_ids = fields.One2many(
        string='Inventario de Registro',
        comodel_name='documentary.control',
        inverse_name='process_id',
    )