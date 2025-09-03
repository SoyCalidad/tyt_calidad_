# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class MgmtCategDocs(models.Model):
    _name = 'mgmt.categ.docs'
    _description = "Mapa de Procesos - Documentos"

    name = fields.Char(string='Nombre', required=True)

class MgmtCateg(models.Model):
    _inherit = 'mgmt.categ'

    type = fields.Many2one(
        'mgmt.categ.type', string='Área',  required=True)
    
    tyt_documents= fields.Many2one(
        'mgmt.categ.docs', string='Documentos')

    tyt_sites_id = fields.Many2one(
        'tyt_studio.sites', string='Ubicación')
    
    referencess = fields.Text(string='Referencias')

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

    type = fields.Many2one(
        'mgmt.categ.type', string='Área', required=True,)

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

    
    # Avoid "False" in "self.type.code"
    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if not self.categ_id:
            return None
        self.type = self.categ_id.type
        if self.type and self.categ_id:
            # type = dict(self._fields['type'].selection).get(self.type)
            type = self.type.code
            code = self.categ_id.code if self.categ_id.code else self.categ_id.name[:2]
            qty = len(self.categ_id.process_ids) + 1
            if type:
                self.code = _("%s-%s-%s") % (type, code, '0' + str(qty))
            else:
                self.code = _("%s-%s") % (code, '0' + str(qty))
    

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