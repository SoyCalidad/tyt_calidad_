from odoo import api, fields, models


class QualityManual(models.Model):
    _inherit = 'mgmtsystem.qualitymanual'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'qualitymanual_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'qualitymanual_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'qualitymanual_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.qualitymanual', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.qualitymanual', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_qualitymanual.action_mgmtsystem_qualitymanual').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class QualityManualValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    qualitymanual_elaboration_id = fields.Many2one(
        'mgmtsystem.qualitymanual', string='Padre')
    qualitymanual_review_id = fields.Many2one(
        'mgmtsystem.qualitymanual', string='Padre')
    qualitymanual_validation_id = fields.Many2one(
        'mgmtsystem.qualitymanual', string='Padre')
