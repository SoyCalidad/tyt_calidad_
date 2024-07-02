from odoo import api, fields, models


class InitialEvaluation(models.Model):
    _inherit = 'evaluation.initial_evaluation'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'initial_evaluation_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'initial_evaluation_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'initial_evaluation_validation_id', string='Validación')

    parent_edition = fields.Many2one(
        comodel_name='evaluation.initial_evaluation', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='evaluation.initial_evaluation', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_partner_qualification.initial_evaluation_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class InitialEvaluationValidationStep(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    initial_evaluation_elaboration_id = fields.Many2one(
        'evaluation.initial_evaluation', string='Evaluación inicial (Elaboración)')
    initial_evaluation_review_id = fields.Many2one(
        'evaluation.initial_evaluation', string='Evaluación inicial (Revisión)')
    initial_evaluation_validation_id = fields.Many2one(
        'evaluation.initial_evaluation', string='Evaluación inicial (Validación)')
