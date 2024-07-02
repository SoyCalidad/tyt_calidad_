from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Target(models.Model):
    _inherit = 'mgmtsystem.target'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'target_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'target_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'target_validation_id', string='Validación')
    
    process_id = fields.Many2one(
        'mgmt.categ', string='Proceso')


class TargetValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    target_elaboration_id = fields.Many2one(
        'mgmtsystem.target', string='Padre')
    target_review_id = fields.Many2one(
        'mgmtsystem.target', string='Padre')
    target_validation_id = fields.Many2one(
        'mgmtsystem.target', string='Padre')
