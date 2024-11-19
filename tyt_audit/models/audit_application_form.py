# -*- coding: utf-8 -*-

from odoo import fields, models, api, http
from odoo.http import request
from odoo.exceptions import ValidationError
import base64

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

        if request.httprequest.method == "POST":
            # Guardar los datos ingresados en el formulario
            planning_record.write({
                "finding": kwargs.get("finding", ""),
                "non_conformity_wording": kwargs.get("non_conformity_wording", "").strip(),
            })

            # Manejar los archivos adjuntos
            attachments = request.httprequest.files.getlist('attachment')
            attachment_ids = []
            for attachment in attachments:
                if attachment.content_type not in ['application/pdf', 'image/jpeg', 'image/png']:
                    return request.make_response(
                        "Solo se permiten archivos PDF, JPEG o PNG.",
                        status=400
                    )

                if len(attachment.read()) > 100 * 1024:  # 100 KB
                    return request.render('tyt_audit.error_template', {
                        'error_message': "El archivo adjunto no debe exceder los 100 KB."
                    })

                attached_file = request.env['ir.attachment'].create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'audit.audit.planning',
                    'res_id': planning_id,
                })
                attachment_ids.append(attached_file.id)

            # Actualizar el registro con los archivos adjuntos
            planning_record.write({
                'evidence_attachment_ids': [(4, attachment_id) for attachment_id in attachment_ids]
            })

            # Redirigir sin enviar un diccionario como segundo argumento
            return request.redirect('/audit_application/%d/' % planning_id)

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
        finding = planning_record.finding or ""
        norm = (
            ", ".join(planning_record.iso_9001_standards_ids.mapped("combined_name"))
            if planning_record.iso_9001_standards_ids
            else ""
        )
        evidence = "\n".join(planning_record.evidence_attachment_ids.mapped('name')) if planning_record.evidence_attachment_ids else ""
        audit_week = planning_record.audit_audit_id.audited_week or ""
        audit_date = planning_record.audit_audit_id.audit_date or ""
        center = (
            planning_record.audit_audit_id.tyt_sites_related_id.display_name
            if planning_record.audit_audit_id and planning_record.audit_audit_id.tyt_sites_related_id
            else "Sin Sitio"
        )
        non_conformity_wording = planning_record.non_conformity_wording or ""

        context = {
            "audit": {
                "procedure": procedure or "",
                "clause": clause or "",
                "responsible": responsible or "",
                "verification": verification or "",
                "audited": audited or "",
                "audit_group": audit_group or "",
                "norm": norm or "",
                "evidence": evidence or "",
                "audit_week": audit_week or "",
                "audit_date": audit_date or "",
                "center": center or "",
                "non_conformity_wording": non_conformity_wording or "",
            },
            "planning_id": planning_id,
        }

        return request.render("tyt_audit.audit_application_form_template", context)
