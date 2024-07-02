import calendar
import logging
from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import Warning


class SwotWizard(models.TransientModel):
    _name = "wizard.swot.report"

    swot_id = fields.Many2one(
        'mgmtsystem.context.swot', 
        string='Matriz FODA',
        domain=[('state', '!=', 'cancel')])

    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'swot': self.swot_id.id,
            'is_wizard': True,
            'model': 'wizard.swot.report',
            'res_model': 'wizard.swot.report',
        }
        return self.env.ref('mgmtsystem_context.report_swot').report_action(self, data=datas)

