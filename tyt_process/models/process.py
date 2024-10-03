# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class ProcessInherit(models.Model):
    _inherit = 'mgmt.process'

    documentarycontrol_ids = fields.One2many(
        string='Inventario de Registro',
        comodel_name='documentary.control',
        inverse_name='process_id',
    )

    #### Change String : Edición to Versión #####

    last_edition = fields.Html(
        string=u'Versión vigente',
        compute='_compute_last_edition',
    )

    @api.depends('name')
    def _compute_last_edition(self):
        for record in self:
            document = self.env['process.edition'].search([
                ('process_id', '=', record.id),
                ('active', '=', True)
            ], order='numero desc', limit=1)
            if document:
                if str(document.id).isdigit():
                    record.real_last_edition = document.id
                record.last_edition = _("<a data-oe-id=%s data-oe-model='process.edition' href=#id=%s&model=process.edition>%s</a>") % (
                    document.id, document.id, document.numero,)
                record.validate_date = document.date_validate
            else:
                record.last_edition = 'No existe versión vigente'
                record.real_last_edition = None
                record.validate_date = None

    '''
    @api.model
    def create(self, values):
        # Verificar si 'name' está en values para evitar errores
        if 'name' in values:
            # Crear la secuencia con el nuevo prefijo
            sequence = self.env['ir.sequence'].sudo().create({
                'name': 'Secuencia de ' + values.get('name'),
                'active': True,
                'prefix': 'Versión-nro.',
                'padding': 4,
                'number_next': 1,
                'number_increment': 1,
            })
            values['sequence_id'] = sequence.id
        # Llamar al método create original
        result = super(ProcessInherit, self).create(values)
        return result
    '''