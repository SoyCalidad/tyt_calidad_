from odoo import api, fields, models
from collections import defaultdict


class ProcessEditionReport(models.AbstractModel):
    _name = 'report.mgmtsystem_process.report_process_edition_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data.get('model') and data['model'] == 'mgmt.process_edition.report.wizard':
            if data['id']:
                process_edition = self.env['process.edition'].browse(data['id'])
        else:
            process_edition = self.env['process.edition'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': process_edition,
        }
