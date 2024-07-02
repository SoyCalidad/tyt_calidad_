from odoo import api, fields, models


class ProcessCategType(models.Model):
    _inherit = 'mgmt.categ.type'

    state = fields.Selection(string='Estado', selection=[(
        'draft', 'Borrador'), ('validate_ok', 'Validado'), ], default='draft')
    user_id = fields.Many2one(
        string='Responsable',
        comodel_name='res.users',
        ondelete='cascade',
        default=lambda self: self.env.user and self.env.user.id or False,
    )

    @api.model
    def action_open_process_categ_type(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_process.action_process_categ_type_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_process_categ_type_step(self):
        """ Set the onboarding step as done """
        self.state = 'validate_ok'
        pass

    def send_validate_ok(self):
        self.state = 'validate_ok'
        self.env.company.sudo().set_onboarding_step_done(
            'process_categ_type_onboarding_state')


class ProcessCateg(models.Model):
    _inherit = 'mgmt.categ'

    @api.model
    def action_open_process_categ(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_process.action_process_categ_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_process_categ_step(self):
        """ Set the onboarding step as done """
        self.state = 'validate_ok'
        pass


class ProcessProcess(models.Model):
    _inherit = 'mgmt.process'

    state = fields.Selection(string='Estado', selection=[(
        'draft', 'Borrador'), ('validate_ok', 'Validado'), ], default='draft')
    user_id = fields.Many2one(
        string='Responsable',
        comodel_name='res.users',
        ondelete='cascade',
        default=lambda self: self.env.user and self.env.user.id or False,
    )

    @api.model
    def action_open_process_process(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_process.action_process_process_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_process_process_step(self):
        """ Set the onboarding step as done """
        self.state = 'validate_ok'
        pass

    def send_validate_ok(self):
        self.state = 'validate_ok'
        self.env.company.sudo().set_onboarding_step_done(
            'process_process_onboarding_state')


class ProcessEdition(models.Model):
    _inherit = 'process.edition'

    @api.model
    def action_open_process_edition(self, action_ref=None):
        if not action_ref:
            action_ref = 'mgmtsystem_process.action_process_edition_configurator'
        return self.env.ref(action_ref).read()[0]

    def action_save_onboarding_process_edition_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.env.company.sudo().set_onboarding_step_done(
            'process_edition_onboarding_state')
