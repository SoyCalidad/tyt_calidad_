# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class MgmtCateg(models.Model):
    _inherit = 'mgmt.categ'

    attachment_ids = fields.Many2many('ir.attachment', string='Archivos')

    def write(self, vals):
        res = super(MgmtCateg, self).write(vals)
        for record in self:
            domain = [
                ('res_model', '=', 'mgmt.categ'),
                ('res_id', '=', record.id)
            ]
            attachments = self.env['ir.attachment'].search(domain)
            record.attachment_ids = [(6, 0, attachments.ids)]
        return res




'''
    attachment_ids = fields.Many2many('ir.attachment', string='Archivos', compute='_compute_attachments')

    def _get_attachment_domain(self):
        self.ensure_one()
        return [
            ('res_model', '=', 'mgmt.categ'),
            ('res_id', '=', self.id)
        ]

    def _compute_attachments(self):
        for record in self:
            domain = record._get_attachment_domain()
            attachments = self.env['ir.attachment'].search(domain)
            record.attachment_ids = [(6, 0, attachments.ids)]
'''