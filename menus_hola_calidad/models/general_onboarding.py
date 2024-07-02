# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import calendar
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError, RedirectWarning
from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    # general dashboard onboarding
    general_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    general_analysis_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    general_plan_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    general_do_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    general_check_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    general_act_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_general_plan(self, action_ref=None):
        if not action_ref:
            action_ref = 'menus_hola_calidad.action_general_plan_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_general_general(self, action_ref=None):
        if not action_ref:
            action_ref = 'menus_hola_calidad.action_general_general_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_general_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.general_onboarding_state = 'closed'

    def get_and_update_general_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'general_analysis_onboarding_state',
            'general_plan_onboarding_state',
            'general_do_onboarding_state',
            'general_check_onboarding_state',
            'general_act_onboarding_state'
        ]
        return self.sudo().get_and_update_onbarding_state('general_onboarding_state', steps)

    @api.model
    def action_verify_general_analysis(self):
        diagnostic = self.env['hola_calidad.diagnostic'].search(
            [('state', '=', 'validate')])
        if diagnostic:
            self.env.company.sudo().set_onboarding_step_done(
                'general_analysis_onboarding_state')
        else:
            res = []
            l = [diagnostic]
            for each in l:
                if not each:
                    res.append(each._description)
            msg = '\n'.join(res)
            f_msg = 'Los módulos no están validados:\n' + msg
            raise ValidationError(f_msg)

    @api.model
    def action_verify_general_plan(self):
        context_internal_issue = self.env['mgmtsystem.context.internal_issue'].search(
            [('state', '=', 'validate_ok')])
        context_external_issue = self.env['mgmtsystem.context.external_issue'].search(
            [('state', '=', 'validate_ok')])
        context_swot = self.env['mgmtsystem.context.swot'].search(
            [('state', '=', 'validate_ok')])
        context_pest = self.env['mgmtsystem.context.pest'].search(
            [('state', '=', 'validate_ok')])
        context_stakeholders = self.env['mgmtsystem.stakeholders'].search(
            [('state', '=', 'validate_ok')])
        context_policy = self.env['mgmtsystem.context.policy'].search(
            [('state', '=', 'validate_ok')])

        process_categ_type = self.env['mgmt.categ.type'].search(
            [('state', '=', 'validate_ok')])
        process_categ = self.env['mgmt.categ.type'].search(
            [('state', '=', 'validate_ok')])
        process_process = self.env['mgmt.process'].search(
            [('state', '=', 'validate_ok')])
        process_edition = self.env['process.edition'].search(
            [('state', '=', 'validate_ok'), ('active', '=', True)])

        matrix_risk = self.env['matrix.matrix'].search(
            [('state', '=', 'validate_ok'), ('type', '=', 'risk')])
        matrix_opportunity = self.env['matrix.matrix'].search(
            [('state', '=', 'validate_ok'), ('type', '=', 'opportunity')])
        risk = self.env['matrix.block.line'].search(
            [('state', '=', 'validate'), ('type', '=', 'risk')])
        opportunity = self.env['matrix.block.line'].search(
            [('state', '=', 'validate'), ('type', '=', 'opportunity')])

        legal_legal = self.env['legal.legal'].search(
            [('state', '=', 'validate_ok')])

        if context_external_issue and context_stakeholders and context_internal_issue and context_swot and context_pest and context_policy and process_categ and process_categ_type and process_process and process_edition and risk and opportunity and matrix_risk and matrix_opportunity and legal_legal:
            self.env.company.sudo().set_onboarding_step_done(
                'general_plan_onboarding_state')
        else:
            res = []
            l = [context_external_issue, context_stakeholders, context_internal_issue, context_swot, context_pest, context_policy, process_categ,
                 process_categ_type, process_process, process_edition, risk, opportunity, matrix_risk, matrix_opportunity, legal_legal]
            for each in l:
                if not each:
                    res.append(each._description)
            msg = '\n'.join(res)
            f_msg = 'Los módulos no están validados:\n' + msg
            raise ValidationError(f_msg)
    
    @api.model
    def action_verify_general_do(self):
        comunication_plan = self.env['comunication.plan'].search(
            [('state', '=', 'validate_ok')])
        comunication_meeting = self.env['record.meeting'].search(
            [('state', '=', 'close')])
        training_plan = self.env['mgmtsystem.plan.training'].search(
            [('state', '=', 'validate_ok')])
        training_training = self.env['mgmtsystem.plan.training.line'].search(
            [('state', '=', 'validate_ok')])
        maintenance_plan = self.env['mgmtsystem.maintenance.plan'].search(
            [('state', '=', 'validate_ok')])
        maintenance_maintenance = self.env['mgmtsystem.maintenance'].search(
            [('state', '=', 'validate_ok')])

        if comunication_plan and comunication_meeting and training_plan and training_training and maintenance_plan and maintenance_maintenance:
            self.env.company.sudo().set_onboarding_step_done(
                'general_do_onboarding_state')
        else:
            res = []
            l = [comunication_plan, comunication_meeting, training_plan, training_training, maintenance_plan, maintenance_maintenance]
            for each in l:
                if not each:
                    res.append(each._description)
            msg = '\n'.join(res)
            f_msg = 'Los módulos no están validados:\n' + msg
            raise ValidationError(f_msg)

    @api.model
    def action_verify_general_check(self):
        target_target = self.env['mgmtsystem.target'].search(
            [('state', '=', 'closed')])
        target_indicator = self.env['mgmtsystem.indicator'].search(
            [('do_state', '=', 'accomplished')])
        audit_plan = self.env['audit.plan'].search(
            [('state', '=', 'validate_ok')])
        audit_audit = self.env['audit.audit'].search(
            [('state', '=', 'final')])
        mgmt_review_plan = self.env['management.review.plan'].search(
            [('state', '=', 'validate_ok')])
        mgmt_review_review = self.env['management.review'].search(  
            [('state', '=', 'validate_ok')])

        if target_target and target_indicator and audit_plan and audit_audit and mgmt_review_plan and mgmt_review_review:
            self.env.company.sudo().set_onboarding_step_done(
                'general_check_onboarding_state')
        else:
            res = []
            l = [target_target, target_indicator, audit_plan, audit_audit, mgmt_review_plan, mgmt_review_review]
            for each in l:
                if not each:
                    res.append(each._description)
            msg = '\n'.join(res)
            f_msg = 'Los módulos no están validados:\n' + msg
            raise ValidationError(f_msg)

    @api.model
    def action_verify_general_act(self):
        nc = self.env['mgmtsystem.nonconformity'].search(
            [('state', '=', 'done')])
        action = self.env['mgmtsystem.action'].search(
            [('state', '=', 'done')])
        if nc and action:
            self.env.company.sudo().set_onboarding_step_done(
                'general_act_onboarding_state')
        else:
            res = []
            l = [nc, action]
            for each in l:
                if not each:
                    res.append(each._description)
            msg = '\n'.join(res)
            f_msg = 'Los módulos no están validados:\n' + msg
            raise ValidationError(f_msg)


class GeneralCheck(models.Model):
    _name = 'general.check'

    def action_save_onboarding_general_plan_step(self):
        """ Set the onboarding step as done """
        pass
