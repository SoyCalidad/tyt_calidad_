from odoo import api, fields, models
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class ReportWizard(models.TransientModel):
    _name = 'mgmtsystem.report_wizard'
    _description = 'Wizard para Reportes'

    def action_print_parameters(self, report_id, objects):
        try:
            ids = objects.ids
            return self.env.ref(report_id).report_action(ids)
        except Exception:
            _logger.error('No se pudo descargar el reporte')
            raise UserError("Error al generar el reporte")
