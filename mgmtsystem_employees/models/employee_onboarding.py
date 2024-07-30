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

    # employee dashboard onboarding
    hr_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    hr_department_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the hr department onboarding panel", default='not_done')
    hr_job_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the hr job onboarding panel", default='not_done')
    hr_employee_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the hr employee onboarding panel", default='not_done')
    # hr_orgchart_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
    #     'done', "Done"), ('closed', "Closed")], string="State of the hr organization chart onboarding panel", default='not_done')

    @api.model
    def action_open_hr_department(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_employees.action_hr_department_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_hr_job(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_employees.action_hr_job_configurator'
        return self.env.ref(action_ref).read()[0]
    
    @api.model
    def action_open_hr_employee(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_employees.action_hr_employee_configurator'
        return self.env.ref(action_ref).read()[0]
    
    # @api.model
    # def action_open_hr_orgchart(self, action_ref=None):
    #     if not action_ref:
    #         action_ref = 'mgmtsystem_employees.action_hr_orgchart_configurator'
    #     return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_employee_onboarding(self):
        """ Mark the hr onboarding panel as closed. """
        self.env.company.employee_onboarding_state = 'just_done'

    def get_and_update_employee_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'hr_department_onboarding_state',
            'hr_job_onboarding_state',
            'hr_employee_onboarding_state',
            # 'hr_orgchart_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('hr_onboarding_state', steps)


class HrDepartment(models.Model):
    _inherit = 'hr.department'
    #_rec_name = 'name'

    def action_save_onboarding_hr_department_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate(self):
        super().send_validate()
        self.env.company.sudo().set_onboarding_step_done(
            'hr_department_onboarding_state')


class HrJob(models.Model):
    _inherit = 'hr.job'

    def action_save_onboarding_hr_job_step(self):
        """ Set the onboarding step as done """
        pass

    @api.onchange('employee_id')
    def send_final(self):
        super().send_final()
        self.env.company.sudo().set_onboarding_step_done(
            'hr_job_onboarding_state')
        
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def action_save_onboarding_hr_employee_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate(self):
        super().send_validate()
        self.env.company.sudo().set_onboarding_step_done(
            'hr_employee_onboarding_state')


# class HrOrgChart(models.Model):
#     _inherit = 'mgmtsystem.plan.employee'

#     def action_save_onboarding_employee_employee_step(self):
#         """ Set the onboarding step as done """
#         pass

#     @api.onchange('employee_id')
#     def send_final(self):
#         super().send_final()
#         self.env.company.sudo().set_onboarding_step_done(
#             'employee_employee_onboarding_state')

