# -*- coding: utf-8 -*-
import base64
import io
import os
import time
from datetime import datetime

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class OrganizationChart(models.AbstractModel):
    _name = 'report.mgmtsystem_context.organization_chart_report'
    

    @api.model
    def _get_report_values(self, docids, data=None):
            return {
                'doc_ids': self.ids,
                'time': time,
            }
