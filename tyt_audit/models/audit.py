# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError, Warning

from odoo import http
from odoo.http import request
import base64


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

    def action_open_audit_application_form(self):
        planning_id = self.id  # ID de la línea de planificación actual

        # Construye la URL pasando el ID de la planificación
        url = f"/audit_application/{planning_id}/"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }

    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Evidencia",
        help="Archivos adjuntos relacionados con esta planificación.",
    )

    def action_next_record(self):
        # Guardar el registro actual
        self.ensure_one()
        self.write({"state": "completed"})  # Cambiar el estado si es necesario

        # Lógica para avanzar al siguiente registro
        next_record = self.search([("id", ">", self.id)], limit=1)
        if next_record:
            # Redirigir al siguiente registro
            return {
                "type": "ir.actions.act_url",
                "url": f"/audit_application/{next_record.id}/",
                "target": "self",
            }
        else:
            # Mensaje si no hay más registros
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Fin de las secciones",
                    "message": "No hay más registros para revisar.",
                    "type": "info",
                    "sticky": False,
                },
            }


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

    clause_id = fields.Many2one(
        "audit.audit.planning.clause",
        string="Cláusula",
        default=lambda self: self.env.context.get("default_clause_id"),
    )
    iso_9001_standards_ids = fields.Many2many(
        "audit.audit.planning.iso9001_standard",
        string="Norma ISO 9001:2015",
        default=lambda self: self.env.context.get("default_iso_9001_standards_ids"),
    )

    def action_generate(self):
        # Por ahora, simplemente cierra el formulario o agrega una lógica simple
        return {"type": "ir.actions.act_window_close"}


class AuditApplicationController(http.Controller):

    @http.route(
        "/audit_application/<int:planning_id>/",
        type="http",
        auth="user",
        website=True,
        csrf=False,
        methods=["GET", "POST"],
    )
    def audit_application_form(self, planning_id, **kwargs):
        planning_record = request.env["audit.audit.planning"].sudo().browse(planning_id)

        if (
            request.httprequest.method == "POST"
            and "attachment" in request.httprequest.files
        ):
            file_storage = request.httprequest.files.getlist("attachment")
            for file in file_storage:
                file_content = file.read()
                attachment = (
                    request.env["ir.attachment"]
                    .sudo()
                    .create(
                        {
                            "name": file.filename,
                            "type": "binary",
                            "datas": base64.b64encode(file_content),
                            "res_model": "audit.audit.planning",
                            "res_id": planning_record.id,
                        }
                    )
                )

        # Resto del código para extraer datos y renderizar el formulario
        procedure = (
            planning_record.audit_audit_id.tyt_procedure_description_id.name
            if planning_record.audit_audit_id.tyt_procedure_description_id
            else ""
        )
        clause = planning_record.clause_id.name if planning_record.clause_id else ""
        responsible = (
            planning_record.employee_id.name if planning_record.employee_id else ""
        )
        verification = planning_record.verification or ""
        audited = planning_record.audit_audit_id.employee_ids.mapped("name")
        audited = ", ".join(audited) if audited else ""
        audit_group = (
            planning_record.audit_audit_id.team_id.name
            if planning_record.audit_audit_id.team_id
            else ""
        )
        finding = planning_record.finding or "good_practice"
        norm = (
            ", ".join(planning_record.iso_9001_standards_ids.mapped("name"))
            if planning_record.iso_9001_standards_ids
            else ""
        )
        evidence = (
            planning_record.evidence_id.name if planning_record.evidence_id else ""
        )
        audit_week = planning_record.audit_audit_id.audited_week or ""
        audit_date = planning_record.audit_audit_id.audit_date or ""
        center = (
            planning_record.audit_audit_id.tyt_sites_related_id.name
            if planning_record.audit_audit_id.tyt_sites_related_id
            and hasattr(planning_record.audit_audit_id.tyt_sites_related_id, "name")
            else ""
        )

        comment = planning_record.comment or ""
        evaluation = planning_record.evaluation or ""

        context = {
            "audit": {
                "procedure": procedure,
                "clause": clause,
                "responsible": responsible,
                "verification": verification,
                "audited": audited,
                "audit_group": audit_group,
                "finding": finding,
                "norm": norm,
                "evidence": evidence,
                "audit_week": audit_week,
                "audit_date": audit_date,
                "center": center,
                "comment": comment,  # Agregado aquí
                "evaluation": evaluation,  # Agregado aquí
            },
            "planning_id": planning_id,
        }

        return request.render("tyt_audit.audit_application_form_template", context)
