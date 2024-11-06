# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DocumentaryControl(models.Model):
    _name = 'documentary.control.tyt_docs'

    name = fields.Char()
    abbreviation = fields.Char(string="Abreviatura")

class DocumentaryControl(models.Model):
    _inherit = 'documentary.control'

    process_last_edition = fields.Char(
        compute='_compute_process_last_edition', string='Versión', readonly=True)
    reception_date = fields.Date(string='Fecha de Recepción')
    sender_id = fields.Many2one('res.partner', string='Remitente')
    received_by_id = fields.Many2one('hr.employee', string='Persona que lo Recibió')

    area_id = fields.Many2one('mgmt.categ.type', string='Área Responsable')
    tyt_document_id = fields.Many2one('documentary.control.tyt_docs', string='Documento')
    int_code = fields.Char(
        string='Código',
        copy=False,
    )

    @api.onchange('area_id','tyt_document_id')
    def _onchange_int_code(self):
        if not self.area_id or not self.tyt_document_id:
            return
        next_number = self.id
        self.int_code = ("%s-%s-%s") % (self.tyt_document_id.abbreviation, self.area_id.code, str(next_number))    