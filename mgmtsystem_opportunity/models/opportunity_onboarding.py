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

    # opportunity dashboard onboarding
    opportunity_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    opportunity_matrix_opp_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    opportunity_matrix_risk_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    opportunity_opp_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    opportunity_risk_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    def get_and_update_opportunity_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'opportunity_matrix_opp_onboarding_state',
            'opportunity_matrix_risk_onboarding_state',
            'opportunity_opp_onboarding_state',
            'opportunity_risk_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('opportunity_onboarding_state', steps)

    @api.model
    def action_open_opportunity_matrix_opp(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_opportunity.action_opportunity_matrix_opp_configurator'
        result = self.env.ref(action_ref).read()[0]
        result['context'] = {'default_type':'opportunity'}
        return result

    @api.model
    def action_open_opportunity_matrix_risk(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_opportunity.action_opportunity_matrix_risk_configurator'
        result = self.env.ref(action_ref).read()[0]
        result['context'] = {'default_type':'risk'}
        return result

    @api.model
    def action_open_opportunity_opp(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_opportunity.action_opportunity_opp_configurator'
        result = self.env.ref(action_ref).read()[0]
        result['context'] = {'default_type':'opportunity'}
        return result

    @api.model
    def action_open_opportunity_risk(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_opportunity.action_opportunity_risk_configurator'
        result = self.env.ref(action_ref).read()[0]
        result['context'] = {'default_type':'risk'}
        return result

    @api.model
    def action_close_opportunity_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        pass
        # self.env.company.opportunity_onboarding_state = 'closed'


class OpportunityMatrix(models.Model):
    _inherit = 'matrix.matrix'

    def action_save_onboarding_opportunity_matrix_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        if self.type == 'risk':
            self.env.company.sudo().set_onboarding_step_done(
                'opportunity_matrix_risk_onboarding_state')
        if self.type == 'opportunity':
            self.env.company.sudo().set_onboarding_step_done(
                'opportunity_matrix_opp_onboarding_state')


class OpportunityMatrixLine(models.Model):
    _inherit = 'matrix.block.line'

    def action_save_onboarding_opportunity_matrix_line_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate(self):
        super().send_validate()
        if self.type == 'risk':
            self.env.company.sudo().set_onboarding_step_done(
                'opportunity_risk_onboarding_state')
        if self.type == 'opportunity':
            self.env.company.sudo().set_onboarding_step_done(
                'opportunity_opp_onboarding_state')
