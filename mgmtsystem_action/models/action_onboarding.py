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

    # action dashboard onboarding
    action_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    action_action_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_action_action(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_action.action_action_action_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_action_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.action_onboarding_state = 'closed'

    def get_and_update_action_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'action_action_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('action_onboarding_state', steps)


class ActionAction(models.Model):
    _inherit = 'mgmtsystem.action'

    def action_save_onboarding_action_plan_step(self):
        """ Set the onboarding step as done """
        pass

    def send_done(self):
        super().send_done()
        self.env.company.sudo().set_onboarding_step_done(
            'action_action_onboarding_state')
