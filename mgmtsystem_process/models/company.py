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

    # process dashboard onboarding
    process_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    process_categ_type_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    process_categ_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    process_process_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    process_edition_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_process_categ_type(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_process.action_process_categ_type_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_process_categ(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_process.action_process_categ_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_process_process(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_process.action_process_process_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_process_edition(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_process.action_process_edition_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_process_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        pass
        # self.env.company.process_onboarding_state = 'not_done'

    def get_and_update_process_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'process_categ_type_onboarding_state',
            'process_categ_onboarding_state',
            'process_process_onboarding_state',
            'process_edition_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('process_onboarding_state', steps)
