from odoo import api, fields, models


class ImprovePlanMatrix(models.Model):
    _inherit = 'soycalidad.improve_plan.matrix'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'improve_plan_matrix_elaboration_id', string='Elaboración', copy=True)
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'improve_plan_matrix_review_id', string='Revisión', copy=True)
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'improve_plan_matrix_validation_id', string='Validación', copy=True)

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    parent_edition = fields.Many2one(
        comodel_name='soycalidad.improve_plan.matrix', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='soycalidad.improve_plan.matrix', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'soycalidad_improve.improve_plan_matrix_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class ImprovePlanMatrixValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    improve_plan_matrix_elaboration_id = fields.Many2one(
        'soycalidad.improve_plan.matrix', string='Padre')
    improve_plan_matrix_review_id = fields.Many2one(
        'soycalidad.improve_plan.matrix', string='Padre')
    improve_plan_matrix_validation_id = fields.Many2one(
        'soycalidad.improve_plan.matrix', string='Padre')
