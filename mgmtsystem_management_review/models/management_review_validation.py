from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ManagementReviewPlan(models.Model):
    _inherit = 'management.review.plan'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmt_review_plan_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmt_review_plan_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmt_review_plan_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    parent_edition = fields.Many2one(
        comodel_name='management.review.plan', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='management.review.plan', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_management_review.mgmtsystem_review_plan_action1').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def send_elaborate(self):
        super().send_elaborate()
        self.create_child_validation_users(self.line_ids)
        for line in self.line_ids:
            try:
                line.send_elaborate()
            except:
                pass

    def send_review(self):
        super().send_review()
        self.create_child_validation_users(self.line_ids)
        for line in self.line_ids:
            try:
                line.send_review()
            except:
                pass

    def send_validate(self):
        super().send_validate()
        self.create_child_validation_users(self.line_ids)
        for line in self.line_ids:
            try:
                line.send_validate()
            except:
                pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.create_child_validation_users(self.line_ids)
        for line in self.line_ids:
            line.send_validate_ok()

    def send_cancel(self):
        super().send_cancel()
        for line in self.line_ids:
            try:
                line.send_cancel()
            except:
                pass


class ManagementeReview(models.Model):
    _inherit = 'management.review'

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('tracked', 'En proceso'),
            ('closed', 'Terminado'),
            ('cancel', 'Obsoleto')
        ],
        default='elaborate',
        copy=False,
    )

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmt_review_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmt_review_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmt_review_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    parent_edition = fields.Many2one(
        comodel_name='management.review', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='management.review', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def send_tracked(self):
        for each in self:
            each.state = 'tracked'

    def send_closed(self):
        for each in self:
            each.state = 'closed'

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_management_review.action_management_review').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class ManagementeReviewValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    mgmt_review_plan_elaboration_id = fields.Many2one(
        'management.review.plan', string='Padre')
    mgmt_review_plan_review_id = fields.Many2one(
        'management.review.plan', string='Padre')
    mgmt_review_plan_validation_id = fields.Many2one(
        'management.review.plan', string='Padre')

    mgmt_review_elaboration_id = fields.Many2one(
        'management.review', string='Padre')
    mgmt_review_review_id = fields.Many2one(
        'management.review', string='Padre')
    mgmt_review_validation_id = fields.Many2one(
        'management.review', string='Padre')
