from odoo import api, fields, models


class StockInspection(models.Model):
    _inherit = 'stock.inspection'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'stock_inspection_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'stock_inspection_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'stock_inspection_validation_id', string='Validación')

    parent_edition = fields.Many2one(
        comodel_name='stock.inspection', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='stock.inspection', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'stock_inspection.stock_inspection_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class StockInspectionValidationStep(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    stock_inspection_elaboration_id = fields.Many2one(
        'stock.inspection', string='Evaluación de compra (Elaboración)')
    stock_inspection_review_id = fields.Many2one(
        'stock.inspection', string='Evaluación de compra (Revisión)')
    stock_inspection_validation_id = fields.Many2one(
        'stock.inspection', string='Evaluación de compra (Validación)')
