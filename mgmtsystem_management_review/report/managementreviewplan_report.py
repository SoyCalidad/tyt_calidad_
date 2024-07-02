from odoo import api, fields, models


class MangnamentReviewPlanReport(models.AbstractModel):
    _name = 'report.mgmtsystem_management_review.review_plan_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        company = self.env.user.company_id
        if data and data.get('is_wizard'):
            if data['id']:
                management_review_plan = self.env['management.review.plan'].browse(data['id'])
        else:
            management_review_plan = self.env['management.review.plan'].browse(docids)

        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': management_review_plan,
        }


class MangnamentReviewPlanReportWizard(models.TransientModel):
    _name = "wizard.mgmtsystem_management_reviewplan.report"

    management_review_plan = fields.Many2one('management.review.plan', string='Programa de revisiones por la dirección', required=True)

    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'id': self.management_review_plan.id,
            'is_wizard': True,
            'model': 'wizard.mgmtsystem_management_reviewplan.report',
            'res_model': 'wizard.mgmtsystem_management_reviewplan.report',
        }
        return self.env.ref('mgmtsystem_management_review.reporte').report_action(self, data=datas)