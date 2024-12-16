# -*- coding: utf-8 -*-

from odoo import fields, models, api, http
from odoo.http import request
from odoo.exceptions import ValidationError
import base64
from odoo.exceptions import UserError, ValidationError

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
        "/audit_application/<int:audit_audit_id>/<int:audit_form_id>/",
        type="http",
        auth="user",
        website=True,
        csrf=False,
        methods=["GET", "POST"],
    )
    def audit_application_form(self, audit_audit_id, audit_form_id, **kwargs):
        # Verifica que ambos registros existen
        audit = request.env["audit.audit"].sudo().browse(audit_audit_id)
        planning_record = request.env["audit.audit.planning"].sudo().browse(audit_form_id)

        if not audit.exists():
            return request.not_found()

        if not planning_record.exists():
            return request.not_found()

        if planning_record.audit_audit_id.id != audit_audit_id:
            return request.not_found()

        if request.httprequest.method == "POST":
            # Manejar los archivos adjuntos
            attachments = request.httprequest.files.getlist('attachment')
            attachment_ids = []
            for attachment in attachments:
                file_content = attachment.read()  # Leer el contenido del archivo solo una vez

                # Validar si el archivo contiene datos
                # if not file_content:
                #     raise UserError(f"El archivo {attachment.filename} está vacío.")

                # Validar el tamaño del archivo
                if len(file_content) > 20 * 1024 * 1024:  # 20 MB
                    raise UserError(f"El archivo {attachment.filename} excede los 20 MB.")

                # Validar el tipo de archivo
                # if attachment.content_type not in ['application/pdf', 'image/jpeg', 'image/png']:
                #     raise UserError(f"El tipo de archivo {attachment.content_type} no está permitido.")

                # Crear el adjunto en `ir.attachment` usando `datas`
                attached_file = request.env['ir.attachment'].create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(file_content),  # Codificar el contenido en Base64
                    'mimetype': attachment.content_type,  # Guardar el tipo MIME
                    'res_model': 'audit.audit.planning',
                    'res_id': audit_form_id,
                })
                attachment_ids.append(attached_file.id)

            # Actualizar el registro con los archivos adjuntos y guardar el comentario de no conformidad solo si se envió
            update_values = {
                'evidence_attachment_ids': [(4, attachment_id) for attachment_id in attachment_ids],
            }

            # Actualizar 'comment' solo si existe en los datos POST
            if "comment" in kwargs:
                update_values["comment"] = kwargs.get("comment", "").strip()
            # Capturar y guardar `finding`
            if "finding" in kwargs:
                update_values["finding"] = kwargs.get("finding", "").strip()

            planning_record.write(update_values)

            # Redirigir a la misma página actualizada
            return request.redirect('/audit_application/%d/%d/' % (audit_audit_id, audit_form_id))

        # Resto del código para extraer datos y renderizar el formulario
        procedure = planning_record.audit_audit_id.tyt_procedure_description_id.name or ""
        clause = planning_record.clause_id.name or ""
        responsible = planning_record.new_job_id.name or ""
        verification = planning_record.verification or ""
        audited = ", ".join(planning_record.audit_audit_id.employee_ids.mapped("name")) or ""
        audit_group = planning_record.audit_audit_id.team_id.name or ""
        finding = planning_record.finding or ""
        norm = ", ".join(planning_record.iso_9001_standards_ids.mapped("combined_name")) or ""
        evidence_char = planning_record.evidence_char or ""
        evidence = "\n".join(planning_record.evidence_attachment_ids.mapped("name")) or ""
        audit_week = planning_record.audit_audit_id.audited_week or "0"
        audit_date = planning_record.audit_audit_id.audit_date or "Sin Fecha"
        center = planning_record.audit_audit_id.tyt_sites_related_id.display_name or "Sin Sitio"
        comment = planning_record.comment or ""

        # Obtener todas las URLs válidas desde los botones "Generar Auditoría"
        valid_urls = self.get_valid_urls(audit_audit_id)

        # Buscar el índice de la URL actual en la lista de válidas
        current_url = f"/audit_application/{audit_audit_id}/{audit_form_id}/"
        try:
            current_index = valid_urls.index(current_url)
            next_url = valid_urls[current_index + 1]  # Obtener la siguiente URL válida
        except (ValueError, IndexError):
            next_url = None  # No hay más registros válidos

        context = {
            "audit": {
                "procedure": procedure or "",
                "clause": clause or "",
                "responsible": responsible or "",
                "verification": verification or "",
                "audited": audited or "",
                "audit_group": audit_group or "",
                "finding": finding or "",
                "norm": norm or "",
                "evidence_char": evidence_char or "",
                "evidence": evidence or "",
                "audit_week": audit_week or "",
                "audit_date": audit_date or "",
                "center": center or "",
                "comment": comment or "",
            },
            "audit_form_id": audit_form_id,
            "audit_audit_id": audit_audit_id,
            "next_url": next_url if next_url else None,
        }

        return request.render("tyt_audit.audit_application_form_template", context)
        
    def get_valid_urls(self, audit_audit_id):
        """
        Retorna una lista de URLs válidas basadas en los registros que tienen el campo `audit_audit_id`.
        """
        valid_urls = []
        planning_records = request.env["audit.audit.planning"].sudo().search([
            ("audit_audit_id", "=", audit_audit_id)
        ], order="id")

        for record in planning_records:
            if record.audit_audit_id:
                valid_urls.append(f"/audit_application/{audit_audit_id}/{record.id}/")

        return valid_urls


    def action_next_record(self, audit_audit_id, audit_form_id):
        """
        Redirige al siguiente registro válido basado en las URLs con el botón "Generar Auditoría".
        """
        valid_urls = self.get_valid_urls(audit_audit_id)
        current_url = f"/audit_application/{audit_audit_id}/{audit_form_id}/"
        try:
            current_index = valid_urls.index(current_url)
            next_url = valid_urls[current_index + 1]
        except (ValueError, IndexError):
            next_url = None

        if next_url:
            return request.redirect(next_url)
        else:
            return request.render("web.message", {
                "title": "Fin de los registros",
                "message": "No hay más registros para revisar en esta actividad.",
            })