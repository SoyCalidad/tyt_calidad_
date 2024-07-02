from odoo import _, api, fields, models


class SWOTReport(models.AbstractModel):
    _name = 'report.mgmtsystem_context.report_swot_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            swot_id = self.env['mgmtsystem.context.swot'].browse(
                data['swot'])
        else:
            swot_id = swot_id = self.env['mgmtsystem.context.swot'].browse(
                docids)

        company = self.env.user.company_id

        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': swot_id,
        }
