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

    # nonconformity dashboard onboarding
    nonconformity_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    nonconformity_nonconformity_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_nonconformity_nonconformity(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_nonconformity.action_nonconformity_nonconformity_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_nonconformity_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.nonconformity_onboarding_state = 'closed'

    def get_and_update_nonconformity_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'nonconformity_nonconformity_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('nonconformity_onboarding_state', steps)


class NonconformityNonconformity(models.Model):
    _inherit = 'mgmtsystem.nonconformity'

    def action_save_onboarding_nonconformity_nonconformity_step(self):
        """ Set the onboarding step as done """
        pass

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'done':
            self.env.company.sudo().set_onboarding_step_done(
                'nonconformity_nonconformity_onboarding_state')
