from odoo import api, fields, models
from collections import defaultdict


class ComplaintReport(models.AbstractModel):
    _name = 'report.mgmtsystem_qualitymanual.report_qualitymanual'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            qualitymanual = self.env['mgmtsystem.qualitymanual'].browse(data['qlty'])
        else:
            qualitymanual = self.env['mgmtsystem.qualitymanual'].browse(docids)
        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': qualitymanual,
        }
