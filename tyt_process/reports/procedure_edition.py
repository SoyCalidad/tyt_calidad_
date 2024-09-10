import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TYTProcedureEditionReport(models.AbstractModel):
    _name = 'report.tyt_process.report_procedure_edition_tyt'
    _description = 'TYT Procedure Edition Report'

    @api.model
    def _get_report_values(self, docids, data=None):

        return {
            'doc_ids': docids,
            'doc_model': 'process.edition',
            'docs': self.env['process.edition'].browse(docids),
            'data': data,
        }