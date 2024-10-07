from odoo import api, fields, models


class AuditPlan(models.Model):
    _inherit = 'audit.plan.tyt.auditor'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'audit_plan_tyt_auditor_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'audit_plan_tyt_auditor_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'audit_plan_tyt_auditor_validation_id', string='Validación')



class AuditPlanValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    audit_plan_tyt_auditor_elaboration_id = fields.Many2one(
        'audit.plan.tyt.auditor', string='Padre (Elaboración)')
    audit_plan_tyt_auditor_review_id = fields.Many2one(
        'audit.plan.tyt.auditor', string='Padre (Revisión)')
    audit_plan_tyt_auditor_validation_id = fields.Many2one(
        'audit.plan.tyt.auditor', string='Padre (Validación)')