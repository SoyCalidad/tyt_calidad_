from odoo import fields, models, api, _
from odoo.exceptions import Warning
from datetime import date, datetime
import calendar
from dateutil.relativedelta import relativedelta
import logging


class wizard_stakeholder(models.TransientModel):
    _name = "wizard.stakeholder.report"
    
    stakeholder_matrix_id = fields.Many2one('mgmtsystem.stakeholders', string='Matriz de interesados')

    def action_print(self):
        data = self.read()[0]
        datas = {
            'ids': self._ids,
            'stakeholders': self.stakeholder_matrix_id.id,
            'model': 'wizard.stakeholder.report',
            'res_model': 'wizard.stakeholder.report',
        }
        a = self.env.ref('mgmtsystem_context.report_stakeholders').report_action(self.stakeholder_matrix_id)
        return a

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
