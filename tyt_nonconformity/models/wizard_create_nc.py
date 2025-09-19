from odoo import models, fields, api, _
from odoo.exceptions import UserError

class TYTNC(models.TransientModel):
    _inherit = 'wizard.create.nc'

    @api.onchange('report_id')
    def _onchange_report_id(self):
        """Cargar automáticamente líneas de hallazgos 'No Conformidad'"""
        if not self.report_id:
            return

        # Buscar líneas con `finding = non_conformity` en el modelo `audit.audit.planning`
        lines = self.env['audit.audit.planning'].sudo().search([
            ('audit_report_id', '=', self.report_id.id),
            ('finding', '=', 'non_conformity'),
        ])

        # Validar si hay líneas encontradas
        if not lines:
            raise UserError(
                _("No se encontró ninguna 'No conformidad' en este informe de auditoría. "
                  "Por favor, asegúrese de que la lista de verificación esté completa y que los datos sean correctos.")
            )

        # Crear las líneas nuevas sin limpiar manualmente
        line_vals = []
        for line in lines:
            line_vals.append((0, 0, {
                'name': line.comment or '-',  # Usar el valor de `comment` en lugar de otros valores
                'type_id': line.clause_id.id if line.clause_id else False,
                'auditor_id': line.employee_id.id if line.employee_id else False,
                'team_id': False,  # Si no tienes un campo relacionado, deja esto en `False`
                'date_found': fields.Date.today(),  # Puedes usar `line.date_found` si está definido
                'details': line.comment or '',  # Descripción del hallazgo
            }))

        # Reemplazar directamente las líneas existentes con las nuevas
        self.update({'wline_ids': line_vals})

    def create_nonconformity(self):
        """Crear registros en el módulo de mejora"""
        for line in self.wline_ids:
            # Crear los datos de la no conformidad
            data = {
                'report_id': self.report_id.id,
                'name': line.name,
                'type_id': line.type_id.id,
                'partner_id': line.auditor_id.id if line.auditor_id else None,
                'audit_team_id': line.team_id.id if line.team_id else None,
                'date_found': line.date_found,
                'description': line.details or '',
                'process_id': line.process_id.id if line.process_id else None,
                'finding': 'non_conformity',
            }
            self.env['mgmtsystem.nonconformity'].create(data)

        # Cambiar el estado del informe de auditoría
        self.report_id.write({'state': 'in_process'})
