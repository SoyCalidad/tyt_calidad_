from odoo import api, fields, models


class MatrixMatrix(models.Model):
    _inherit = 'matrix.matrix'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'matrix_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'matrix_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'matrix_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class MatrixValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    matrix_elaboration_id = fields.Many2one(
        'matrix.matrix', string='Padre')
    matrix_review_id = fields.Many2one(
        'matrix.matrix', string='Padre')
    matrix_validation_id = fields.Many2one(
        'matrix.matrix', string='Padre')


class MatrixBlockLine(models.Model):
    _inherit = 'matrix.block.line'

    def button_new_version(self):
        super().button_new_version()
        self.state = 'draft'
