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

    # audit dashboard onboarding
    audit_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    audit_plan_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    audit_audit_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    audit_report_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the audit report onboarding ", default='not_done')

    @api.model
    def action_open_audit_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_audit.action_audit_plan_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_audit_audit(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_audit.action_audit_audit_configurator'
        return self.env.ref(action_ref).read()[0]
    
    @api.model
    def action_open_audit_report(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_audit.action_audit_report_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_audit_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.audit_onboarding_state = 'closed'

    def get_and_update_audit_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'audit_plan_onboarding_state',
            'audit_audit_onboarding_state',
            'audit_report_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('audit_onboarding_state', steps)


class AuditPlan(models.Model):
    _inherit = 'audit.plan'

    def action_save_onboarding_audit_plan_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'audit_plan_onboarding_state')


class Auditaudit(models.Model):
    _inherit = 'audit.audit'

    def action_save_onboarding_audit_audit_step(self):
        """ Set the onboarding step as done """
        pass

    def send_final(self):
        super().send_final()
        self.env.company.sudo().set_onboarding_step_done(
            'audit_audit_onboarding_state')

class AuditReport(models.Model):
    _inherit = 'audit.report'

    def action_save_onboarding_audit_report_step(self):
        """ Set the onboarding step as done """
        pass

    def send_final(self):
        super().send_final()
        self.env.company.sudo().set_onboarding_step_done(
            'audit_report_onboarding_state')

