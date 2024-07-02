from odoo import api, fields, models


class TrainingPlan(models.Model):
    _inherit = 'mgmtsystem.plan'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'training_elaboration_id', string='Elaboración', copy=True)
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'training_review_id', string='Revisión', copy=True)
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'training_validation_id', string='Validación', copy=True)

    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.plan', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.plan', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_audit.audit_plan_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class TrainingPlanValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    training_elaboration_id = fields.Many2one(
        'mgmtsystem.plan', string='Padre')
    training_review_id = fields.Many2one(
        'mgmtsystem.plan', string='Padre')
    training_validation_id = fields.Many2one(
        'mgmtsystem.plan', string='Padre')
