# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

class AuditPlanning(models.Model):
    _name = "audit.audit.planning.template"
    _description = "Lista de Verificación / Planificación / Template"

    name = fields.Char(
        string='Nombre'
    )

    audit_audit_id = fields.Many2one(
        'audit.audit',
        string="Lista de verificación",
        store=True
    )

    # audit_report_id = fields.Many2one(
    #     'audit.report',
    #     string="Informe de Auditoría",
    #     store=True
    # )

    iso_9001_standards_ids = fields.Many2many(
        'audit.audit.planning.iso9001_standard',
        'audit_audit_planning_template_iso9001_standard_rel',  # Nombre tabla relacional
        'planning_id',  # columna que referencia al modelo actual
        'standard_id',  # olumna que referencia al modelo Many2many        
        string='Normas ISO 9001:2015'
    )

    iso_9001_combined_names = fields.Text(
        string='Norma ISO 9001:2015 (Denominación completa)',
        compute='_compute_iso_9001_combined_names',
        store=True
    )

    @api.depends('iso_9001_standards_ids')
    def _compute_iso_9001_combined_names(self):
        for record in self:
            # Combina los nombres de todas las normas seleccionadas
            combined_names = ', '.join(record.iso_9001_standards_ids.mapped('combined_name'))
            record.iso_9001_combined_names = combined_names

    clause_id = fields.Many2one(
        string='Cláusula',
        comodel_name='audit.audit.planning.clause'
    )

    # employee_id = fields.Many2one(
    #     string='Auditor Responsable',
    #     comodel_name='hr.employee',
    # )

    new_job_id = fields.Many2one(
        string='Responsable',
        comodel_name='hr.job',
        # related='employee_id.job_id',
        # store=True,
        # readonly=True,
    )

    verification = fields.Char(string='Verificación')

    finding = fields.Selection(
        selection=[
            ("non_conformity", "No Conformidad"),
            ("good_practices", "Buenas Prácticas"),
        ],
        string="Hallazgo",
    )

    evidence_char = fields.Char(
        string='Evidencia'
        )
    

    tyt_procedure_description_id = fields.Many2one(
        string='Procedimiento',
        comodel_name='audit.plan.schedule.descriptions',
    )

    tyt_procedure_activity_id = fields.Many2one(
        string='Actividad',
        comodel_name='audit.plan.schedule.activities',
        domain="[('description_id', '=', tyt_procedure_description_id)]",
    )