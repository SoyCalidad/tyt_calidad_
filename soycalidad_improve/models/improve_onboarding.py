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

    # improve dashboard onboarding
    improve_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    improve_plan_change_request = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the change request invoice onboarding ", default='not_done')
    improve_plan_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    improve_improve_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_change_request(self, action_ref=None):
        if not action_ref:
            action_ref = 'soycalidad_improve.action_change_request_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_improve_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'soycalidad_improve.action_improve_plan_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_improve_improve(self, action_ref=None):
        if not action_ref:
            action_ref = 'soycalidad_improve.action_improve_improve_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_improve_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.improve_onboarding_state = 'closed'

    def get_and_update_improve_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'improve_plan_onboarding_state',
            'improve_improve_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('improve_onboarding_state', steps)


class ChangeRequest(models.Model):
    _inherit = 'soycalidad.change_request'

    def action_save_onboarding_change_request_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'change_request_onboarding_state')


class ImprovePlanMatrix(models.Model):
    _inherit = 'soycalidad.improve_plan.matrix'

    def action_save_onboarding_improve_plan_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'improve_improve_onboarding_state')


class ImprovePlan(models.Model):
    _inherit = 'soycalidad.improve_plan'

    def action_save_onboarding_improve_improve_step(self):

        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'improve_plan_onboarding_state')



