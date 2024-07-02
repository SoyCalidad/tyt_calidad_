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

    # legal dashboard onboarding
    legal_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    legal_plan_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    legal_legal_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_legal_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_legal.action_legal_plan_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_legal_legal(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_legal.action_legal_legal_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_legal_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.legal_onboarding_state = 'closed'

    def get_and_update_legal_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'legal_plan_onboarding_state',
            'legal_legal_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('legal_onboarding_state', steps)


class LegalPlan(models.Model):
    _inherit = 'legal.plan'

    def action_save_onboarding_legal_plan_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'legal_plan_onboarding_state')


class LegalLegal(models.Model):
    _inherit = 'legal.legal'

    def action_save_onboarding_legal_legal_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate(self):
        super().send_validate()
        self.env.company.sudo().set_onboarding_step_done(
            'legal_legal_onboarding_state')
