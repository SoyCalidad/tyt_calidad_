from odoo import api, fields, models


class LegalPlan(models.Model):
    _inherit = 'legal.plan'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'legal_plan_elaboration_id', string='Elaboración', copy=True)
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'legal_plan_review_id', string='Revisión', copy=True)
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'legal_plan_validation_id', string='Validación', copy=True)

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class LegalPlanValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    legal_plan_elaboration_id = fields.Many2one(
        'legal.plan', string='Padre')
    legal_plan_review_id = fields.Many2one(
        'legal.plan', string='Padre')
    legal_plan_validation_id = fields.Many2one(
        'legal.plan', string='Padre')
