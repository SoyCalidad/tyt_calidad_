# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class AuditAudit(models.Model):
    _inherit = 'audit.audit'

    # Controla visibilidad de boton "start_process_audit_audit"
    is_process_started = fields.Boolean(
        string='Proceso Iniciado',
        default=False
    )

    def start_process_audit_audit(self):
        """
        Crea registros en 'audit.audit.planning' usando datos de 'audit.audit.planning.template'
        que cumplan las condiciones especificadas.
        """
        self.ensure_one() # Asegurarse de que solo se está trabajando con un registro

        # Verificar que los campos obligatorios estén seleccionados
        if not self.tyt_procedure_description_id or not self.tyt_procedure_activity_id:
            raise ValidationError("Debe seleccionar un Procedimiento y una Actividad antes de ejecutar el proceso.")

        # Buscar registros en 'audit.audit.planning.template' que coincidan con los valores
        # de 'tyt_procedure_description_id' y 'tyt_procedure_activity_id' del registro actual
        templates = self.env['audit.audit.planning.template'].search([
            ('tyt_procedure_description_id', '=', self.tyt_procedure_description_id.id),
            ('tyt_procedure_activity_id', '=', self.tyt_procedure_activity_id.id),
        ])

        # Verificar si se encontraron registros coincidentes
        if not templates:
            raise ValidationError("No se encontraron registros en los 'templates' de Lista de Verificación que coincidan con el 'Procedimiento' y la 'Actividad' seleccionados. Por favor, verifique su elección e inténtelo de nuevo.")
        
        # Crear registros en 'audit.audit.planning' con los datos obtenidos
        for template in templates:
            self.env['audit.audit.planning'].create({
                'tyt_procedure_description_id': template.tyt_procedure_description_id.id,
                'tyt_procedure_activity_id': template.tyt_procedure_activity_id.id,
                'iso_9001_standards_ids': [(6, 0, template.iso_9001_standards_ids.ids)],  # Relación Many2many
                'clause_id': template.clause_id.id,
                'new_job_id': template.new_job_id.id,
                'verification': template.verification,
                'finding': template.finding,
                'evidence_char': template.evidence_char,
                'audit_audit_id': self.id,  # Relacionar con el registro actual de 'audit.audit'
            })

        # Marcar el proceso como iniciado
        self.is_process_started = True