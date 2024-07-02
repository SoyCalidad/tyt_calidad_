from odoo import api, fields, models


class EvaluationValidation(models.Model):
    _inherit = 'res.partner.evaluation'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'evaluation_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'evaluation_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'evaluation_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    parent_edition = fields.Many2one(
        comodel_name='res.partner.evaluation', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='res.partner.evaluation', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_partner_qualification.action_res_partner_evaluation').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class AudievaluationValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    evaluation_elaboration_id = fields.Many2one(
        'res.partner.evaluation', string='Padre')
    evaluation_review_id = fields.Many2one(
        'res.partner.evaluation', string='Padre')
    evaluation_validation_id = fields.Many2one(
        'res.partner.evaluation', string='Padre')
