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

    # complaints dashboard onboarding
    complaints_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    complaints_internal_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    complaints_external_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_complaints_internal(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_complaints.action_complaints_internal_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_complaints_external(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_complaints.action_complaints_external_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_complaints_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.complaints_onboarding_state = 'closed'

    def get_and_update_complaints_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'complaints_internal_onboarding_state',
            'complaints_external_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('complaints_onboarding_state', steps)


class ComplaintComplaint(models.Model):
    _inherit = 'complaint.complaint'

    def action_save_onboarding_complaints_internal_step(self):
        """ Set the onboarding step as done """
        pass

    def action_save_onboarding_complaints_external_step(self):
        """ Set the onboarding step as done """
        pass
        
    @api.onchange('state')
    def _onchange_state(self):
        super()._onchange_state()
        if self.state == 'done' and self.type == 'supplier':
            self.env.company.sudo().set_onboarding_step_done(
                'complaints_external_onboarding_state')
        if self.state == 'done' and self.type == 'customer':
            self.env.company.sudo().set_onboarding_step_done(
                'complaints_internal_onboarding_state')
