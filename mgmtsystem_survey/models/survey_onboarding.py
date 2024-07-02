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


class ResCompanyEmployeeOnboarding(models.Model):
    _inherit = "res.company"

    # employee dashboard onboarding
    survey_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the survey onboarding panel", default='not_done')
    survey_survey_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the survey onboarding panel", default='not_done')

    @api.model
    def action_open_survey_survey(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_survey.action_survey_survey_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_survey_onboarding(self):
        """ Mark the hr onboarding panel as closed. """
        self.env.company.employee_onboarding_state = 'just_done'

    def get_and_update_survey_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'survey_survey_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('survey_onboarding_state', steps)


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    def action_save_onboarding_survey_survey_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate(self):
        super().send_validate()
        self.env.company.sudo().set_onboarding_step_done(
            'survey_survey_onboarding_state')
