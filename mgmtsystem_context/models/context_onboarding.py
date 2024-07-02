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

    # context dashboard onboarding
    context_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the context onboarding panel", default='not_done')
    context_internal_issue_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the context onboarding panel", default='not_done')
    context_external_issue_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the context onboarding panel", default='not_done')
    context_swot_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the context onboarding panel", default='not_done')
    context_pest_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the context onboarding panel", default='not_done')
    context_stakeholders_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the context onboarding panel", default='not_done')
    context_policy_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the context onboarding panel", default='not_done')

    @api.model
    def action_open_context_internal_issue(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_internal_issue_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_context_external_issue(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_external_issue_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_context_swot(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_swot_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_context_pest(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_pest_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_context_stakeholders(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_stakeholders_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_context_policy(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_policy_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_context_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.sudo().context_onboarding_state = 'closed'

    def get_and_update_context_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'context_internal_issue_onboarding_state',
            'context_external_issue_onboarding_state',
            'context_swot_onboarding_state',
            'context_pest_onboarding_state',
            'context_stakeholders_onboarding_state',
            'context_policy_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('context_onboarding_state', steps)


class ContextInternalIssue(models.Model):
    _inherit = 'mgmtsystem.context.internal_issue'

    @api.model
    def action_open_context_internal_issue(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_internal_issue_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_context_internal_issue_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'context_internal_issue_onboarding_state')


class ContextExternalIssue(models.Model):
    _inherit = 'mgmtsystem.context.external_issue'

    @api.model
    def action_open_context_external_issue(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_external_issue_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_context_external_issue_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'context_external_issue_onboarding_state')


class ContextSWOT(models.Model):
    _inherit = 'mgmtsystem.context.swot'

    @api.model
    def action_open_context_swot(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_swot_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_context_swot_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'context_swot_onboarding_state')


class ContextPEST(models.Model):
    _inherit = 'mgmtsystem.context.pest'

    @api.model
    def action_open_context_pest(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_pest_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_context_pest_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'context_pest_onboarding_state')


class ContextStakeholders(models.Model):
    _inherit = 'mgmtsystem.stakeholders'

    @api.model
    def action_open_context_stakeholders(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_stakeholders_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_context_stakeholders_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'context_stakeholders_onboarding_state')


class ContextPolicy(models.Model):
    _inherit = 'mgmtsystem.context.policy'

    @api.model
    def action_open_context_policy(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_context.action_context_policy_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_context_policy_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'context_policy_onboarding_state')
