# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError, Warning

class AuditProcedure(models.Model):
    _name = "audit.audit.procedure"
    _description = "Procedimiento de Lista de Verificación"

    name = fields.Char(
        string='Nombre',
        required=True,
    )

class Audit(models.Model):
    _inherit = "audit.audit"

    #plan_id = many2one "audit.plan"
        # Creo que debería quitar el ondelete cascade, porque se podrían borrar actividades y datos de otros modelos independientes, SON MODELOS INDEPENDIENTES

    '''
    audit_plan_id = fields.Many2one(
        string='Programa',
        comodel_name='audit.plan',
    )
    '''
    tyt_sites_related_id = fields.Many2one(
        'x_sitios',
        string='Sitio',
        related='plan_id.sites_id',
        store=True,
        readonly=True,
    )

    employee_id = fields.Many2one(
        string='Auditor',
        comodel_name='hr.employee',
    )

    tyt_procedure_id = fields.Many2one(
        string='Procedimiento',
        comodel_name='audit.audit.procedure',
    )

    job_id = fields.Many2one(
        string='Responsable',
        comodel_name='hr.job',
    )

    audit_date = fields.Date(
        string='Fecha de Auditoría',
    )

    audited_week = fields.Integer(
        string='Semana Auditada',
        default=0,
    )