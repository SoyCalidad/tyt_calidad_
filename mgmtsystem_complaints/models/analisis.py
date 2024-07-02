# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ComplaintComplaintCauseWhy(models.Model):
    _name = 'complaint.complaint.cause_why'
    _description = 'Complaint Complaint Cause Why'
    

class Analisis(models.Model):
    _name = 'complaint.analisis'
    _description = 'Análisis de reclamos'

    name = fields.Char(
        string='Referencia',
        required=True,
    )
    elaborate_ids = fields.Many2one(
        string=u'Elaborado',
        comodel_name='res.users',
        default=lambda self: self.env.user
    )
    date = fields.Datetime(
        string='Fecha de inicialización',
        default=fields.Datetime.now,
        readonly=True,
        store=True,
    )
    close = fields.Boolean(
        string='Incluir reclamos terminadas',
    )

    type = fields.Selection(
        string='Tipo',
        selection=[
            ('customer', 'Cliente'), 
            ('supplier', 'Proveedor')],
    )

    filter = fields.Selection(
        string='Filtrar por',
        selection=[
            ('none', 'Todas las reclamos pendientes'),
            ('date', 'Entre un rango de fechas'),
            ('categ', 'Un tipo de reclamo'),
            ('state', 'Estado de reclamo'),
            ('partial', 'Seleccionar manualmente')],
        default='none',
    )

    date_init = fields.Date(
        string='Fecha inicio',
    )
    date_fin = fields.Date(
        string='Fecha final',
    )

    categ_id = fields.Many2one(
        string='Tipo',
        comodel_name='complaint.categ',
    )

    complaint_state = fields.Selection(
        string='Estado',
        selection=[
            ('open', 'Abierto'),
            ('in_process', 'En proceso'),
            ('close', 'Cerrado'),
            ('cancel', 'Cancelado')],
    )
    state = fields.Selection(
        string='Estado',
        selection=[
            ('draft', 'Borrador'),
            ('in_process', 'En proceso'),
            ('close', 'Cerrado'),
            ('cancel', 'Cancelado')],
        default='draft',
    )

    complaint_ids = fields.Many2many(
        string='Reclamos',
        comodel_name='complaint.complaint',
        relation='analisis_complaint_rel',
        column1='complaint_id',
        column2='analisis_id',
    )

    def start_filter(self):
        if self.filter == 'none':
            self.complaint_ids = self.env['complaint.complaint'].search([]) or False

        if self.filter == 'date':
            self.complaint_ids = self.env['complaint.complaint'].search([('date_incident','<=',self.date_fin),('date_incident','>=',self.date_init)]) or False

        if self.filter == 'categ':
            self.complaint_ids = self.env['complaint.complaint'].search([('categ_id','=',self.categ_id.id)]) or False

        if self.filter == 'state':
            self.complaint_ids = self.env['complaint.complaint'].search([('state','=',self.complaint_state)]) or False

        if self.filter == 'partial':
            self.complaint_ids = False
        
        self.state = 'in_process'

    def send_close(self):
        self.state = 'close'

    def send_cancel(self):
        self.state = 'cancel'