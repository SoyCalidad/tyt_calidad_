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

class AuditPlanningClause(models.Model):
    _name = "audit.audit.planning.clause"
    _description = "Lista de Verificación / Planificación / Cláusula"

    name = fields.Char(
        string='Nombre',
        required=True,
    )

class AuditPlanningEvidence(models.Model):
    _name = "audit.audit.planning.evidence"
    _description = "Lista de Verificación / Planificación / Evidencia"

    name = fields.Char(
        string='Nombre',
        required=True,
    )


class AuditPlanning(models.Model):
    _name = "audit.audit.planning"
    _description = "Lista de Verificación / Planificación"

    name = fields.Char(
        string='Nombre'
    )

    audit_audit_id = fields.Many2one(
        'audit.audit',
        string="Lista de verificación",
        store=True
    )

    #preguntar
    '''
    iso_9001_standards_ids = fields.Many2many(
        string='Norma ISO 9001:2015',
        comodel_name=''
    )
    '''

    clause_id = fields.Many2one(
        string='Cláusula',
        comodel_name='audit.audit.planning.clause'
    )

    # Afinar
    employee_id = fields.Many2one(
        string='Responsable',
        comodel_name='hr.employee',
    )

    employee_job_id = fields.Many2one(
        comodel_name='hr.job',
        string='Puesto',
        related='employee_id.job_id',
        store=True,
        readonly=True,
    )

    verification = fields.Char(string='Verificación')

    #preguntar
    '''
    findings_id = fields.Many2one(
        string='Hallazgo',
        comodel_name=''
    )
    '''
    evidence_id = fields.Many2one(
            string='Evidencia',
            comodel_name='audit.audit.planning.evidence'
        )
    
    comment = fields.Char(
        string='Comentario'
        )

    evaluation = fields.Char(
        string='Evaluación'
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
    planning_ids = fields.One2many( 
        comodel_name='audit.audit.planning',
        inverse_name='audit_audit_id',
        string='Cronograma')


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

    tyt_procedure_description_id = fields.Many2one(
        string='Procedimiento',
        comodel_name='audit.plan.schedule.descriptions',
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