from odoo import fields, models, api


class ContextScope(models.Model):
    _inherit = 'tyt.context.scope'

    elaboration_step = fields.One2many('mgmtsystem.validation.step', 'scope_elaboration_id', string='Elaboración')
    review_step = fields.One2many('mgmtsystem.validation.step', 'scope_review_id', string='Revisión')
    validation_step = fields.One2many('mgmtsystem.validation.step', 'scope_validation_id', string='Validación')


class ContextScopeValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    scope_elaboration_id = fields.Many2one('tyt.context.scope')
    scope_review_id = fields.Many2one('tyt.context.scope')
    scope_validation_id = fields.Many2one('tyt.context.scope')
