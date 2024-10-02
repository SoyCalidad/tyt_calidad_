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


class ResCompanyEmployeeOnboarding(models.Model):
    _inherit = "res.company"

    @api.model
    def action_open_hr_department(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_employees.action_hr_department_configurator'
        return self.env.ref(action_ref).sudo().read()[0]

    @api.model
    def action_open_hr_job(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_employees.action_hr_job_configurator'
        return self.env.ref(action_ref).sudo().read()[0]
    
    @api.model
    def action_open_hr_employee(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_employees.action_hr_employee_configurator'
        return self.env.ref(action_ref).sudo().read()[0]


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def action_open_training_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_employees.action_training_plan_configurator'
        return self.env.ref(action_ref).sudo().read()[0]

    @api.model
    def action_open_training_training(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_employees.action_training_training_configurator'
        return self.env.ref(action_ref).sudo().read()[0]