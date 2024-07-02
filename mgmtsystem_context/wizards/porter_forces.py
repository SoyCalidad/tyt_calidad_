from odoo import fields, models, api, _
from odoo.exceptions import Warning
from datetime import date, datetime
import calendar
from dateutil.relativedelta import relativedelta
import logging

class PorterForcesReport(models.AbstractModel):
    _name = 'report.mgmtsystem_context.external_issue_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            external_issue_id = self.env['mgmtsystem.context.external_issue'].browse(data['external_issue'])
        else:
            external_issue_id = self.env['mgmtsystem.context.external_issue'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': external_issue_id,
        }

class PorterForcesWizard(models.TransientModel):
    _name = "wizard.porter_forces.report"

    external_issue_id = fields.Many2one('mgmtsystem.context.external_issue',
                                        string='Fuerza de Porter',
                                        domain=[('state', '!=', 'cancel')])

    def action_pdf(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'external_issue': self.external_issue_id.id,
            'is_wizard': True,
            'model': 'wizard.porter_forces.report',
            'res_model': 'wizard.porter_forces.report',
        }
        return self.env.ref('mgmtsystem_context.action_report_external_issue').report_action(self, data=datas)

    def action_print(self):
        data = self.read()[0]
        forces = self.env['mgmtsystem.context.external_issue'].search([])
        datas = {
            'data': data,
            'ids': self._ids,
            'forces': forces,
            'external_issue': self.external_issue_id.id,
            'is_wizard': True,
            'model': 'wizard.porter_forces.report',
            'res_model': 'wizard.porter_forces.report',
        }
        return self.env.ref('mgmtsystem_context.external_issue_report_xls').report_action(self, data=datas)


