from odoo import fields, models, api, _
from odoo.exceptions import Warning
from datetime import date, datetime
import calendar
from dateutil.relativedelta import relativedelta
import logging


class PESTELWizard(models.TransientModel):
    _name = "wizard.pest.report"

    pestel_id = fields.Many2one(
        'mgmtsystem.context.pest',
        string='Contexto organizacional',
        domain=[('state', '!=', 'cancel')])

    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'is_wizard': True,
            'pestel': self.pestel_id.id,
            'model': 'wizard.pest.report',
            'res_model': 'wizard.pest.report',
        }
        return self.env.ref('mgmtsystem_context.action_pest_report').report_action(self, data=datas)

    def action_print_xls(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'is_wizard': True,
            'pestel': self.pestel_id.id,
            'model': 'wizard.pest.report',
            'res_model': 'wizard.pest.report',
        }
        return self.env.ref('mgmtsystem_context.action_pest_xls_report').report_action(self, data=datas)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
