from odoo import api, fields, models


class AuditPlan(models.Model):
    _inherit = 'audit.plan'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'audit_plan_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'audit_plan_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'audit_plan_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    parent_edition = fields.Many2one(
        comodel_name='audit.plan', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='audit.plan', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_audit.audit_plan_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def send_elaborate(self):
        super().send_elaborate()
        self.create_child_validation_users(self.audit_ids)
        for audit in self.audit_ids:
            try:
                audit.send_elaborate()
            except:
                pass

    def send_review(self):
        super().send_review()
        self.create_child_validation_users(self.audit_ids)
        for audit in self.audit_ids:
            try:
                audit.send_review()
            except:
                pass

    def send_validate(self):
        super().send_validate()
        self.create_child_validation_users(self.audit_ids)
        for audit in self.audit_ids:
            try:
                audit.send_validate()
            except:
                pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.create_child_validation_users(self.audit_ids)
        for audit in self.audit_ids:
            audit.send_validate_ok()

    def send_cancel(self):
        super().send_cancel()
        for audit in self.audit_ids:
            try:
                audit.send_cancel()
            except:
                pass


class AuditPlanValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    audit_plan_elaboration_id = fields.Many2one(
        'audit.plan', string='Padre (Elaboración)')
    audit_plan_review_id = fields.Many2one(
        'audit.plan', string='Padre (Revisión)')
    audit_plan_validation_id = fields.Many2one(
        'audit.plan', string='Padre (Validación)')


class AuditAudit(models.Model):
    _inherit = 'audit.audit'

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('send', 'Enviado'),
            ('final', 'Finalizado'),
            ('cancel', 'Obsoleto'),
        ],
        default='elaborate',
        copy=False,
    )

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'audit_audit_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'audit_audit_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'audit_audit_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    parent_edition = fields.Many2one(
        comodel_name='audit.audit', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='audit.audit', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def send_send(self):
        self.write({'state': 'send'})

    def send_final(self):
        self.write({'state': 'final'})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_audit.audit_audit_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class AudiAuditValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    audit_audit_elaboration_id = fields.Many2one(
        'audit.audit', string='Padre (Elaboración)')
    audit_audit_review_id = fields.Many2one(
        'audit.audit', string='Padre (Revisión)')
    audit_audit_validation_id = fields.Many2one(
        'audit.audit', string='Padre (Validación)')
