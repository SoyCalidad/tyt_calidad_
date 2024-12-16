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

    @api.model
    def action_open_change_request(self, action_ref=None):
        if not action_ref:
            action_ref = 'soycalidad_improve.action_change_request_configurator'
        return self.env.ref(action_ref).sudo().read()[0]

    @api.model
    def action_open_improve_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'soycalidad_improve.action_improve_plan_configurator'
        return self.env.ref(action_ref).sudo().read()[0]

    '''
    @api.model
    def action_open_improve_improve(self, action_ref=None):
        if not action_ref:
            action_ref = 'soycalidad_improve.action_improve_improve_configurator'
        return self.env.ref(action_ref).sudo().read()[0]
    '''
    
    ## ACTIONS ##
    @api.model
    def action_open_action_action(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_action.action_action_action_configurator'
        return self.env.ref(action_ref).sudo().read()[0]
    
    ## NON-CONFORMITY ##
    @api.model
    def action_open_nonconformity_nonconformity(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_nonconformity.action_nonconformity_nonconformity_configurator'
        return self.env.ref(action_ref).sudo().read()[0]