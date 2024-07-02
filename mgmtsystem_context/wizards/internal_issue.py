from odoo import fields, models, api, _
from odoo.exceptions import Warning
from datetime import date, datetime
import calendar
from dateutil.relativedelta import relativedelta
import logging


class InternalIssueWizard(models.TransientModel):
    _name = "wizard.internal_issue.report"

    internal_issue_id = fields.Many2one(
        'mgmtsystem.context.internal_issue',
        string='Contexto organizacional',
        domain=[('state', '!=', 'cancel')])

    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'is_wizard': True,
            'internal_issue': self.internal_issue_id.id,
            'model': 'wizard.internal_issue.report',
            'res_model': 'wizard.internal_issue.report',
        }
        return self.env.ref('mgmtsystem_context.report_internal_issue').report_action(self, data=datas)


class InternalIssueReport(models.AbstractModel):
    _name = 'report.mgmtsystem_context.report_internal_issue_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            internal_issue = self.env['mgmtsystem.context.internal_issue'].browse(
                data['internal_issue'])
        else:
            internal_issue = internal_issue = self.env['mgmtsystem.context.internal_issue'].browse(
                docids)

        company = self.env.user.company_id

        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': internal_issue,
        }

