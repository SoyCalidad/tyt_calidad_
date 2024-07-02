# -*- coding: utf-8 -*-


from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    # target dashboard onboarding
    target_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    target_target_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')
    target_indicator_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the account invoice onboarding panel", default='not_done')

    @api.model
    def action_open_target_target(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_target.action_target_target_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_open_target_indicator(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_target.action_target_indicator_configurator'
        return self.env.ref(action_ref).read()[0]

    @api.model
    def action_close_target_onboarding(self):
        """ Mark the invoice onboarding panel as closed. """
        self.env.company.target_onboarding_state = 'closed'

    def get_and_update_target_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'target_target_onboarding_state',
            'target_indicator_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('target_onboarding_state', steps)


class TargetTarget(models.Model):
    _inherit = 'mgmtsystem.target'

    def action_save_onboarding_target_target_step(self):
        """ Set the onboarding step as done """
        pass

    def send_finish(self):
        super().send_finish()
        self.env.company.sudo().set_onboarding_step_done(
            'target_target_onboarding_state')


class TargetIndicator(models.Model):
    _inherit = 'mgmtsystem.indicator'

    def action_save_onboarding_target_indicator_step(self):
        """ Set the onboarding step as done """
        pass

    def do_accomplished(self):
        super().do_accomplished()
        self.env.company.sudo().set_onboarding_step_done(
            'target_indicator_onboarding_state')
