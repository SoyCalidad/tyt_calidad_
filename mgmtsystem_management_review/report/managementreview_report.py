from odoo import api, fields, models


class MangnamentReviewReport(models.AbstractModel):
    _name = 'report.mgmtsystem_management_review.report_managementreview'

    @api.model
    def _get_report_values(self, docids, data=None):
        company = self.env.user.company_id
        if data and data.get('is_wizard'):
            if data['id']:
                management_review = self.env['management.review'].browse(data['id'])
        else:
            management_review = self.env['management.review'].browse(docids)

        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': management_review,
        }


class MangnamentReviewReportWizard(models.TransientModel):
    _name = "wizard.mgmtsystem_management_review.report"

    management_review = fields.Many2one('management.review', string='Revisión por la dirección', required=True)

    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'id': self.management_review.id,
            'is_wizard': True,
            'model': 'wizard.mgmtsystem_management_review.report',
            'res_model': 'wizard.mgmtsystem_management_review.report',
        }
        return self.env.ref('mgmtsystem_management_review.action_report_managementreview2').report_action(self, data=datas)