# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import calendar
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError, RedirectWarning
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT, format_date
from odoo.tools.float_utils import float_round, float_is_zero
from odoo.tools import date_utils
from odoo.tests.common import Form


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def action_open_maintenance_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_maintenance_plan_configurator'
        return self.env.ref(action_ref).sudo().read()[0]

    @api.model
    def action_open_maintenance_maintenance(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_maintenance_maintenance_configurator'
        return self.env.ref(action_ref).sudo().read()[0]

    @api.model
    def action_open_calibration_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_calibration_plan_configurator'
        return self.env.ref(action_ref).sudo().read()[0]

    @api.model
    def action_open_calibration_calibration(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_calibration_calibration_configurator'
        return self.env.ref(action_ref).sudo().read()[0]
