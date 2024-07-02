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

    # comunication dashboard onboarding
    comunication_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    comunication_plan_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    comunication_comunication_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    comunication_record_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_comunication_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_comunication.action_comunication_plan_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_comunication_comunication(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_comunication.action_comunication_comunication_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_comunication_record(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_comunication.action_comunication_record_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_comunication_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.comunication_onboarding_state = 'closed'

    def get_and_update_comunication_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'comunication_plan_onboarding_state',
            'comunication_comunication_onboarding_state',
            'comunication_record_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('comunication_onboarding_state', steps)


class ComunicationPlan(models.Model):
    _inherit = 'comunication.plan'

    def action_save_onboarding_comunication_plan_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'comunication_plan_onboarding_state')


class ComunicationComunication(models.Model):
    _inherit = 'comunication.plan.line'

    def action_save_onboarding_comunication_comunication_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'comunication_comunication_onboarding_state')


class ComunicationRecord(models.Model):
    _inherit = 'record.meeting'

    def action_save_onboarding_comunication_record_step(self):
        """ Set the onboarding step as done """
        pass

    def send_close(self):
        super().send_close()
        self.env.company.sudo().set_onboarding_step_done(
            'comunication_record_onboarding_state')
