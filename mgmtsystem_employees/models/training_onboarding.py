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

    # training dashboard onboarding
    training_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    training_plan_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    training_training_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_training_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_employees.action_training_plan_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_training_training(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_employees.action_training_training_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_training_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.training_onboarding_state = 'closed'

    def get_and_update_training_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'training_plan_onboarding_state',
            'training_training_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('training_onboarding_state', steps)


class TrainingPlan(models.Model):
    _inherit = 'mgmtsystem.plan'

    def action_save_onboarding_training_plan_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate(self):
        super().send_validate()
        self.env.company.sudo().set_onboarding_step_done(
            'training_plan_onboarding_state')


class TrainingTraining(models.Model):
    _inherit = 'mgmtsystem.plan.training'

    def action_save_onboarding_training_training_step(self):
        """ Set the onboarding step as done """
        pass

    @api.onchange('training_id')
    def send_final(self):
        super().send_final()
        self.env.company.sudo().set_onboarding_step_done(
            'training_training_onboarding_state')

