# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


from datetime import tzinfo, date, datetime, timedelta
import pandas as pd

'''
class Frequency(models.Model):
    _name = 'audit.plan.tyt.frequency'
    _description = "Frecuencia de mantenimiento de plan"

    name = fields.Char(
        string='Nombre',
        required=True
    )
    number = fields.Integer(
        string='Cantidad',
        index=True,
        default=15,
        help="Numero de veces que se va a repetir"
    )
    type = fields.Selection(
        string='Periodo',
        selection=[('day', 'Días'), ('week', 'Semana')],
        default='day',
    )
'''
class PlanGeneralScheduleActivities(models.Model):
    _name = "audit.plan.schedule.activities"
    _description = "Cronograma de Auditoría - General / Cronograma / Actividades"

    name = fields.Char(
        string='Nombre',
        required=True
    )

class PlanGeneralScheduleDescriptions(models.Model):
    _name = "audit.plan.schedule.descriptions"
    _description = "Cronograma de Auditoría - General / Cronograma / Descripciones"

    name = fields.Char(
        string='Nombre',
        required=True
    )

class PlanGeneralSchedule(models.Model):
    _name = "audit.plan.schedule"
    _description = "Cronograma de Auditoría - General / Cronograma"

    name = fields.Char(
        string='Nombre',
        required=True
    )

    audit_plan_id = fields.Many2one(
        'audit.plan',
        string="Cronograma de Auditoría",
        store=True
    )

    description_id = fields.Many2one('audit.plan.schedule.descriptions', string='Descripción')

    activity_id = fields.Many2one('audit.plan.schedule.activities', string='Actividades')



    #audit.plan.tyt.auditor
    '''
    audit_plan_schedule_id = fields.Many2one(
        comodel_name="audit.plan",
        string="Cronograma de auditoría - General Vinculado",
        readonly=True,
        store=True,
    )
    '''
    sites_id = fields.Many2one(
        'x_sitios',
        string='Sitio',
    )

    responsible_auditors_id = fields.Many2many(
        'res.partner', string='Auditores Responsables'
    )

    total_weeks = fields.Integer(
        string="Semanas por Auditar",
    )

    @api.constrains('total_weeks')
    def _check_total_weeks_positive(self):
        for record in self:
            if record.total_weeks < 0:
                raise ValidationError(_("'Semanas por Auditar' debe ser un número positivo."))
    '''
    responsible_auditors_id = fields.Many2many(
        related="audit_plan_tyt_auditor_id.schedule_ids.responsible_auditors_id",
        comodel_name="audit.plan",
        string="Auditores Responsables",
        readonly=True,
        store=True,
    )
    
    total_weeks = fields.Many2one(
        related="audit_plan_tyt_auditor_id.schedule_ids.total_sum",
        comodel_name="audit.plan",
        string="Semanas por Auditar",
        readonly=True,
        store=True,
    )
    '''


class Plan(models.Model):
    _inherit = "audit.plan"

    name = fields.Char(
        string='Nombre',
        required=True,
        default="CRONOGRAMA DE AUDITORIA"
    )

    ### CRONOGRAMA DE AUDITORIA - GENERAL

    audit_plan_tyt_auditor_id = fields.Many2one(
        'audit.plan.tyt.auditor',
        string='Nombre de Cronograma - Auditores'
    )

    schedule_ids = fields.One2many( 
        comodel_name='audit.plan.schedule',
        inverse_name='audit_plan_id',
        string='Cronograma')
    

    start_date = fields.Date(
        string='Fecha de inicio',
        required=True,
    )
    limit_date = fields.Date(
        string='Fecha de fin',
        required=True,
    )

    '''
    frequency_id = fields.Many2one(
        string='Frecuencia',
        comodel_name='audit.plan.tyt.frequency',
        copy=True,
    )
    '''

    new_frequency_id = fields.Many2one(
        string='Periodicidad',
        comodel_name='mgmtsystem.frequency',
        required=True,
    )

    new_frequency_id = fields.Many2one(
        string='Periodicidad',
        comodel_name='mgmtsystem.frequency',
        required=True,
    )



    # Campo computado que recopila los IDs de los sitios disponibles
    available_site_ids = fields.Many2many(
        'x_sitios',
        compute='_compute_available_site_ids',
        string='Sitios Disponibles'
    )

    # Campo Many2one para seleccionar un único sitio, restringido por el dominio
    sites_id = fields.Many2one(
        'x_sitios',
        string='Sitio',
        domain="[('id', 'in', available_site_ids)]",
    )

    @api.depends('audit_plan_tyt_auditor_id.schedule_ids.tyt_sites_id')
    def _compute_available_site_ids(self):
        for record in self:
            if record.audit_plan_tyt_auditor_id:
                # Recopila todos los registros de x_sitios vinculados a través de schedule_ids
                sitios = record.audit_plan_tyt_auditor_id.schedule_ids.mapped('tyt_sites_id')
                record.available_site_ids = sitios
            else:
                # Si no hay un auditor asociado, no hay sitios disponibles
                # Asigna un recordset vacío de x_sitios para que el dominio no muestre ningún sitio
                record.available_site_ids = self.env['x_sitios'].browse([])

    @api.onchange('audit_plan_tyt_auditor_id')
    def _onchange_audit_plan_tyt_auditor_id(self):
        if self.audit_plan_tyt_auditor_id:
            # Opcional: Limpiar el campo sites_id si el auditor cambia
            self.sites_id = False
        else:
            self.sites_id = False