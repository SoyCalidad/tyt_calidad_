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

    # maintenance dashboard onboarding
    maintenance_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    maintenance_plan_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    maintenance_maintenance_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    calibration_plan_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    calibration_calibration_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_maintenance_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_maintenance_plan_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_maintenance_maintenance(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_maintenance_maintenance_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_calibration_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_calibration_plan_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_calibration_calibration(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_calibration_calibration_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_maintenance_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.maintenance_onboarding_state = 'closed'

    def get_and_update_maintenance_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'maintenance_plan_onboarding_state',
            'maintenance_maintenance_onboarding_state',
            'calibration_plan_onboarding_state',
            'calibration_calibration_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('maintenance_onboarding_state', steps)


class MaintenancePlan(models.Model):
    _inherit = 'mgmtsystem.maintenance.plan'

    @api.model
    def action_open_maintenance_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_maintenance_plan_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_maintenance_plan_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'maintenance_plan_onboarding_state')


class MaintenanceMaintenance(models.Model):
    _inherit = 'mgmtsystem.maintenance'

    @api.model
    def action_open_maintenance_maintenance(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_maintenance_maintenance_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_maintenance_maintenance_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'maintenance_maintenance_onboarding_state')


class maintenanceSWOT(models.Model):
    _inherit = 'mgmtsystem.calibration.plan'

    @api.model
    def action_open_calibration_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_calibration_plan_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_calibration_plan_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'calibration_plan_onboarding_state')


class maintenancePEST(models.Model):
    _inherit = 'mgmtsystem.calibration'

    @api.model
    def action_open_calibration_calibration(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_infrastructure.action_calibration_calibration_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_calibration_calibration_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'calibration_calibration_onboarding_state')
