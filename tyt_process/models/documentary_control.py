# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DocumentaryControl(models.Model):
    _inherit = 'documentary.control'

    process_last_edition = fields.Char(
        compute='_compute_process_last_edition', string='Versión', readonly=True)
    reception_date = fields.Date(string='Fecha de Recepción')
    sender_id = fields.Many2one('res.partner', string='Remitente')
    received_by_id = fields.Many2one('hr.employee', string='Persona que lo Recibió')