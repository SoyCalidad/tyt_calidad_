# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re

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

    '''
    int_code = fields.Char(
        string='Código',
        copy=False,
        readonly=True,
        compute='_compute_int_code',  # Campo computado
    )
    '''


    int_code = fields.Char(
        string='Código',
        copy=False,
    )

    # int_sequence = fields.Integer(
    #     string='Secuencia',
    #     readonly=True,
    # )

    # @api.depends('tyt_document_id', 'area_id', 'int_sequence')
    # def _compute_int_code(self):
    #     for record in self:
    #         if record.tyt_document_id and record.area_id and record.int_sequence:
    #             # Formato de secuencia con ceros a la izquierda, por ejemplo, '01'
    #             sequence_str = f"{record.int_sequence:02d}"
    #             record.int_code = f"{record.tyt_document_id.abbreviation}{record.area_id.code}-{sequence_str}"
    #         else:
    #             record.int_code = False

    job_id = fields.Many2one('hr.job', string='Responsable')

    tyt_sites_id = fields.Many2one(
        'x_sitios', string='Sitio'
    )


    # @api.onchange('area_id', 'tyt_document_id')
    # def _onchange_int_code(self):
    #     if not self.area_id or not self.tyt_document_id:
    #         return

    #     # Buscar los registros existentes con los mismos tyt_document_id y area_id
    #     existing_records = self.search([
    #         ('tyt_document_id', '=', self.tyt_document_id.id),
    #         ('area_id', '=', self.area_id.id),
    #         ('id', '!=', self.id)  # Excluir el registro actual en caso de edición
    #     ], order='int_sequence desc', limit=1)

    #     if existing_records and existing_records.int_sequence:
    #         self.int_sequence = existing_records.int_sequence + 1
    #     else:
    #         self.int_sequence = 1

    '''
    @api.model
    def create(self, vals):
        # Llamar al super primero para crear el registro y obtener su ID
        record = super(DocumentaryControl, self).create(vals)

        # Si int_sequence no está definido, asignarlo
        if not record.int_sequence:
            existing_records = self.search([
                ('tyt_document_id', '=', record.tyt_document_id.id),
                ('area_id', '=', record.area_id.id),
                ('id', '!=', record.id)
            ], order='int_sequence desc', limit=1)

            if existing_records and existing_records.int_sequence:
                record.int_sequence = existing_records.int_sequence + 1
            else:
                record.int_sequence = 1

            # Recompute int_code después de asignar int_sequence
            record._compute_int_code()

        return record


    def write(self, vals):
        # Si se actualizan tyt_document_id o area_id, recalcular int_sequence
        if 'tyt_document_id' in vals or 'area_id' in vals:
            for record in self:
                existing_records = self.search([
                    ('tyt_document_id', '=', vals.get('tyt_document_id', record.tyt_document_id.id)),
                    ('area_id', '=', vals.get('area_id', record.area_id.id)),
                    ('id', '!=', record.id)
                ], order='int_sequence desc', limit=1)

                if existing_records and existing_records.int_sequence:
                    vals['int_sequence'] = existing_records.int_sequence + 1
                else:
                    vals['int_sequence'] = 1

        result = super(DocumentaryControl, self).write(vals)

        # Recompute int_code después de escribir
        for record in self:
            record._compute_int_code()

        return result
    '''

    @api.onchange('area_id','tyt_document_id')
    def _onchange_int_code(self):
        if not self.area_id or not self.tyt_document_id:
            return
        
        # Convertir self.id a string para manejar tanto IDs reales como temporales
        id_str = str(self.id)
        next_number = ""

        # Usar regex para extraer el número si es un ID temporal (e.g., "NewId_2")
        match = re.match(r'NewId_(\d+)', id_str)
        if match:
            next_number = match.group(1)
        elif id_str.isdigit():
            # Si el ID es un entero (registro ya guardado)
            next_number = id_str

        if next_number.isdigit():
            # Añadir prefijo '0' si hay un número válido
            next_number = '0' + next_number
            # Generar el código completo
            self.int_code = f"{self.tyt_document_id.abbreviation}{self.area_id.code}-{next_number}"
        else:
            # Generar el código sin el número si el registro no está guardado
            self.int_code = f"{self.tyt_document_id.abbreviation}{self.area_id.code}"