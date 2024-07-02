from odoo import fields, models, api, _
from odoo.exceptions import Warning
from datetime import date, datetime
import calendar
from dateutil.relativedelta import relativedelta
import logging


class GeneralWizard(models.TransientModel):
    _name = "wizard.general.report"

    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'model': 'wizard.general.report',
            'res_model': 'wizard.general.report',
        }
        return self.env.ref('mgmtsystem_context.report_general_pdf').report_action(self, data=datas)



class GeneralReport(models.AbstractModel):
        _name = 'report.mgmtsystem_context.report_general_template_pdf'

        @api.model
        def _get_report_values(self, docids, data=None):
            internal_issue_id= self.env['mgmtsystem.context.internal_issue'].search([('state', '=', 'validate_ok')], order='date_elaborate asc', limit=1) or []
            external_issue_id = self.env['mgmtsystem.context.external_issue'].search([('state', '=', 'validate_ok')], order='date_elaborate asc', limit=1) or []
            swot_id = self.env['mgmtsystem.context.swot'].search([('state', '=', 'validate_ok')], order='date_elaborate asc', limit=1) or []
            # policy_id, = self.env['mgmtsystem.context.policy'].search([('state', '=', 'validate_ok')], order='date_elaborate asc', limit=1) or ''
            stakeholder_id = self.env['mgmtsystem.stakeholders'].search([('state', '=', 'validate_ok')], order='date_elaborate asc', limit=1) or []
            company = self.env.user.company_id

            return {
                'doc_ids': self.ids,
                'company': company,
                'internal_issue': internal_issue_id,
                'external_issue_id': external_issue_id,
                'swot_id': swot_id,
                'stakeholder_id': stakeholder_id
            }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
