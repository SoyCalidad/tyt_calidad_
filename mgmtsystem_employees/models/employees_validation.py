from odoo import _, api, fields, models


class TrainingPlan(models.Model):
    _inherit = 'mgmtsystem.plan'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'training_plan_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'training_plan_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'training_plan_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    def send_elaborate(self):
        super().send_elaborate()
        self.create_child_validation_users(self.training_ids)
        for training in self.training_ids:
            try:
                training.send_elaborate()
            except:
                pass

    def send_review(self):
        super().send_review()
        self.create_child_validation_users(self.training_ids)
        for training in self.training_ids:
            try:
                training.send_review(notify=False)
            except:
                pass

    def send_validate(self):
        super().send_validate()
        self.create_child_validation_users(self.training_ids)
        for training in self.training_ids:
            try:
                training.send_validate(notify=False)
            except:
                pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.create_child_validation_users(self.training_ids)
        for training in self.training_ids:
            try:
                training.send_validate_ok()
            except:
                training.state = 'validate_ok'

    def send_cancel(self):
        super().send_cancel()
        for training in self.training_ids:
            try:
                training.send_cancel()
            except:
                pass

    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.plan', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.plan', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_employees.hr_item_plan_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class PlanTraining(models.Model):
    _inherit = 'mgmtsystem.plan.training'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'training_plan_tra_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'training_plan_tra_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'training_plan_tra_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('in_process', 'En proceso'),
            ('final', 'Finalizado'),
            ('caducated', 'Caducado'),
            ('cancel', 'Obsoleto'),
        ],
        default='elaborate',
        copy=False,
    )

    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.plan.training', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.plan.training', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_employees.hr_item_training_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class TrainingPlanValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    training_plan_elaboration_id = fields.Many2one(
        'mgmtsystem.plan', string='Padre')
    training_plan_review_id = fields.Many2one(
        'mgmtsystem.plan', string='Padre')
    training_plan_validation_id = fields.Many2one(
        'mgmtsystem.plan', string='Padre')

    training_plan_tra_elaboration_id = fields.Many2one(
        'mgmtsystem.plan.training', string='Padre')
    training_plan_tra_review_id = fields.Many2one(
        'mgmtsystem.plan.training', string='Padre')
    training_plan_tra_validation_id = fields.Many2one(
        'mgmtsystem.plan.training', string='Padre')
