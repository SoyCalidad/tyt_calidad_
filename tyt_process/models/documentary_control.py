# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re
import logging

_logger = logging.getLogger(__name__)

class DocumentaryControl(models.Model):
    _name = 'documentary.control.tyt_docs'
    _description = "documentary.control.tyt_docs"

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


    job_id = fields.Many2one('hr.job', string='Responsable')

    tyt_sites_id = fields.Many2one(
        'x_sitios', string='Sitio'
    )

    next_number_str = fields.Char(
        string='Next Number',
        compute='_compute_next_number_str',
        store=True,
    )

    code_number_str = fields.Char(
        string='Code Number',
        compute='_compute_code_number_str',
        store=True,
    )

    @api.depends('area_id', 'tyt_document_id')
    def _compute_next_number_str(self):
        for record in self:
            if not record.area_id or not record.tyt_document_id:
                record.next_number_str = ""
                continue
            # Contar los registros existentes con el mismo tyt_document_id y area_id
            count = self.env['documentary.control'].search_count([
                ('tyt_document_id', '=', record.tyt_document_id.id),
                ('area_id', '=', record.area_id.id)
            ])
            # Generar el siguiente número con prefijo '0'
            record.next_number_str = '0' + str(count + 1)

    @api.onchange('area_id','tyt_document_id')
    def _onchange_int_code(self):
        if not self.area_id or not self.tyt_document_id:
            return
        
        self.int_code = f"{self.tyt_document_id.abbreviation}{self.area_id.code}-{self.next_number_str}"





    @api.depends('area_id', 'tyt_document_id', 'next_number_str')
    def _compute_code_number_str(self):
        for record in self:
            if not record.next_number_str:
                record.code_number_str = ""
                continue
            
            try:
                # Remover el prefijo '0' y convertir a entero
                next_number = int(record.next_number_str.lstrip('0') or 0)
                # Asegurarse de que next_number es mayor que 0 para evitar números negativos no deseados
                if next_number > 1:
                    code_number = next_number - 1
                    # Añadir el prefijo '0' nuevamente
                    record.code_number_str = '0' + str(code_number)
                elif next_number == 1:
                    # Si next_number es 1, code_number_str será '00'
                    record.code_number_str = '00'
                else:
                    # Para valores inesperados, dejar el campo vacío
                    record.code_number_str = ""
                
                _logger.info(f"Computed code_number_str for record {record.id}: {record.code_number_str}")
            except ValueError:
                record.code_number_str = ""
                _logger.error(f"Failed to compute code_number_str for record {record.id} due to invalid next_number_str: {record.next_number_str}")


    # @api.onchange('area_id','tyt_document_id')
    # def _onchange_int_code(self):
    #     if not self.area_id or not self.tyt_document_id:
    #         return
        
    #     next_number = len(self.env['documentary.control'].search([
    #         ('tyt_document_id', '=', self.tyt_document_id.id),
    #         ('area_id', '=', self.area_id.id)
    #     ]))
    #     next_number_str = '0' + str(next_number+1)
    #     self.int_code = f"{self.tyt_document_id.abbreviation}{self.area_id.code}-{next_number_str}"

