# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class StakeholderReport(models.AbstractModel):
        _name = 'report.mgmtsystem_context.report_stakeholder_2'

        @api.model
        def _get_report_values(self, docids, data=None):
            stakeholders = self.env['mgmtsystem.stakeholders'].browse(docids)
            company = self.env.user.company_id

            return {
                'doc_ids': self.ids,
                'time': time,
                'docs': stakeholders,
                'company': company,
            }
