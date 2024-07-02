# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class PolicyReport(models.AbstractModel):
        _name = 'report.mgmtsystem_context.politica_de_calidad'

        @api.model
        def _get_report_values(self, docids, data=None):
            if data and data.get('is_wizard'):    
                stakeholders = self.env['mgmtsystem.context.policy'].browse(data['policies'])
            else:
                stakeholders = self.env['mgmtsystem.context.policy'].browse(docids)
                
            company = self.env.user.company_id

            return {
                'doc_ids': self.ids,
                'time': time,
                'docs': stakeholders,
                'company': company,
            }
