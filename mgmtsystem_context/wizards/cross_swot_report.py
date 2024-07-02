from odoo import fields, models, api, _
from odoo.exceptions import Warning
from datetime import date, datetime
import calendar
from dateutil.relativedelta import relativedelta
import logging


class CrossSwotWizard(models.TransientModel):
    _name = "wizard.cross_swot.report"

    cross_swot_id = fields.Many2one(
        'mgmtsystem.context.cross.swot', 
        string='Matriz FODA',
        domain=[('state', '!=', 'cancel')])

    def action_print(self):
        cross_swot_id = self.cross_swot_id.id
        return self.env.ref('mgmtsystem_context.report_cross_swot').report_action(cross_swot_id)



class CrossSwotReport(models.AbstractModel):
        _name = 'report.mgmtsystem_context.report_cross_swot_template'

        @api.model
        def _get_report_values(self, docids, data=None):
            if data and data.get('is_wizard'):
                cross_swot = self.env['mgmtsystem.context.cross.swot'].browse(
                    data['cross_swot'])
            else:
                cross_swot = cross_swot = self.env['mgmtsystem.context.cross.swot'].browse(
                    docids)
            company = self.env.user.company_id
            return {
                'doc_ids': self.ids,
                'company': company,
                'docs': cross_swot,
                'cross_swots': cross_swot,
            }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
