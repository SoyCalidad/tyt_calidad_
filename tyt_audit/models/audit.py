# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError, Warning


class AuditProcedure(models.Model):
    _name = "audit.audit.procedure"
    _description = "Procedimiento de Lista de Verificación"

    name = fields.Char(
        string="Nombre",
        required=True,
    )


class AuditPlanningClause(models.Model):
    _name = "audit.audit.planning.iso9001_standard"
    _description = "Lista de Verificación / Planificación / Cláusula"

    name = fields.Char(
        string="Nombre",
        required=True,
    )

    complete_name = fields.Char(
        string="Nombre",
        required=True,
    )

    combined_name = fields.Char(
        string="Nombre Combinado",
        compute="_compute_combined_name",
        store=True,  # Opcional: almacena el valor en la base de datos
    )

    @api.depends("name", "complete_name")
    def _compute_combined_name(self):
        for record in self:
            if record.name and record.complete_name:
                record.combined_name = f"{record.name} {record.complete_name}"
            else:
                record.combined_name = record.name or record.complete_name


class AuditPlanningClause(models.Model):
    _name = "audit.audit.planning.clause"
    _description = "Lista de Verificación / Planificación / Cláusula"

    name = fields.Char(
        string="Nombre",
        required=True,
    )


class AuditPlanningEvidence(models.Model):
    _name = "audit.audit.planning.evidence"
    _description = "Lista de Verificación / Planificación / Evidencia"

    name = fields.Char(
        string="Nombre",
        required=True,
    )


class AuditPlanning(models.Model):
    _name = "audit.audit.planning"
    _description = "Lista de Verificación / Planificación"

    name = fields.Char(string="Nombre")

    audit_audit_id = fields.Many2one(
        "audit.audit", string="Lista de verificación", store=True
    )

    audit_report_id = fields.Many2one(
        "audit.report", string="Informe de Auditoría", store=True
    )

    iso_9001_standards_ids = fields.Many2many(
        "audit.audit.planning.iso9001_standard", string="Norma ISO 9001:2015"
    )

    clause_id = fields.Many2one(
        string="Cláusula", comodel_name="audit.audit.planning.clause"
    )

    employee_id = fields.Many2one(
        string="Responsable",
        comodel_name="hr.employee",
    )

    employee_job_id = fields.Many2one(
        comodel_name="hr.job",
        string="Puesto de Responsable",
        related="employee_id.job_id",
        store=True,
        readonly=True,
    )

    verification = fields.Char(string="Verificación")

    finding = fields.Selection(
        selection=[
            ("non_conformity", "No Conformidad"),
            ("good_practices", "Buenas Prácticas"),
        ],
        string="Hallazgo",
    )

    evidence_id = fields.Many2one(
        string="Evidencia", comodel_name="audit.audit.planning.evidence"
    )

    comment = fields.Char(string="Comentario")

    evaluation = fields.Char(string="Evaluación")


class Audit(models.Model):
    _inherit = "audit.audit"

    # plan_id = many2one "audit.plan"
    # Creo que debería quitar el ondelete cascade, porque se podrían borrar actividades y datos de otros modelos independientes, SON MODELOS INDEPENDIENTES

    """
    audit_plan_id = fields.Many2one(
        string='Programa',
        comodel_name='audit.plan',
    )
    """
    planning_ids = fields.One2many(
        comodel_name="audit.audit.planning",
        inverse_name="audit_audit_id",
        string="Cronograma",
    )

    month_training = fields.Selection(
        [
            ("1", "Enero"),
            ("2", "Febrero"),
            ("3", "Marzo"),
            ("4", "Abril"),
            ("5", "Mayo"),
            ("6", "Junio"),
            ("7", "Julio"),
            ("8", "Agosto"),
            ("9", "Septiembre"),
            ("10", "Octubre"),
            ("11", "Noviembre"),
            ("12", "Diciembre"),
        ],
        string="Mes elegido",
        required=False,
    )

    observations = fields.Text(
        string="Observaciones/Alcance",
        required=False,
    )

    tyt_sites_related_id = fields.Many2one(
        "x_sitios",
        string="Sitio",
        related="plan_id.sites_id",
        store=True,
        readonly=True,
    )

    employee_id = fields.Many2one(
        string="Auditor",
        comodel_name="hr.employee",
    )

    employee_ids = fields.Many2many(
        string="Auditados",
        comodel_name="hr.employee",
    )

    tyt_procedure_id = fields.Many2one(
        string="Procedimiento",
        comodel_name="audit.audit.procedure",
    )

    tyt_procedure_description_id = fields.Many2one(
        string="Procedimiento",
        comodel_name="audit.plan.schedule.descriptions",
    )

    tyt_procedure_activity_id = fields.Many2one(
        string="Actividad",
        comodel_name="audit.plan.schedule.activities",
        domain="[('description_id', '=', tyt_procedure_description_id)]",
    )
    """
    @api.onchange('tyt_procedure_description_id')
    def _onchange_tyt_procedure_description_id(self):
        if self.tyt_procedure_description_id:
            return {'domain': {'tyt_procedure_activity_id': [('description_id', '=', self.tyt_procedure_description_id.id)]}}
        else:
            return {'domain': {'tyt_procedure_activity_id': []}}
    """

    @api.onchange("tyt_procedure_description_id")
    def _onchange_tyt_procedure_description_id(self):
        if not self.tyt_procedure_description_id:
            self.tyt_procedure_activity_id = False  # Restablece el campo
        return {
            "domain": {
                "tyt_procedure_activity_id": [
                    ("description_id", "=", self.tyt_procedure_description_id.id)
                ]
            }
        }

    job_id = fields.Many2one(
        string="Responsable",
        comodel_name="hr.job",
    )

    audit_date = fields.Date(
        string="Fecha de Auditoría",
    )

    audited_week = fields.Integer(
        string="Semana Auditada",
        default=0,
    )


class AuditGenerationForm(models.TransientModel):
    _name = "audit.generation.form"
    _description = "Formulario de Generación de Auditoría"

    name = fields.Char(string="Nombre")
    date = fields.Date(string="Fecha")

    def action_open_audit_form(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Formulario de Auditoría",
            "view_mode": "form",
            "res_model": "audit.generation.form",
            "target": "new",
        }
