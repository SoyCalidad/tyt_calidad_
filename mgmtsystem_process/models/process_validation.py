from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.http import request


class ProcessEdition(models.Model):
    _inherit = 'process.edition'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'process_edition_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'process_edition_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'process_edition_validation_id', string='Validación')

    def create_notification(self, rank, employees):
        """
        Create a notification from the employees
        """
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (
            self.id, self._name)
        self.env.cr.execute("""SELECT id FROM ir_model 
            WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        else:
            model_id = None
        if rank == 'resp':
            body = 'El procedimiento %s en el que es responsable ha cambiado de versión' % self.process_id.name
        elif rank == 'rel':
            body = 'El procedimiento %s con el que está relacionado ha cambiado de versión' % self.process_id.name
        else:
            body = ''
        for emp in employees:
            if emp.user_id and emp.user_id.partner_id:
                notification_ids = []
                notification_ids.append((0, 0, {
                    'res_partner_id': emp.user_id.partner_id.id,
                    'notification_type': 'inbox'}))
                self.message_post(body=body, message_type='notification',
                                  subtype='mail.mt_comment', notification_ids=notification_ids)

    def notify_to_users(self):
        """
        Notify the validation of the edition to all of their related users
        """
        for edition in self:
            if edition.process_id:
                related_user_ids = edition.process_id.related_employees_ids.employee_ids
                responsible_user_ids = edition.process_id.responsible_id.employee_ids
                self.create_notification('rel', related_user_ids)
                self.create_notification('resp', responsible_user_ids)

    def send_validate_ok(self):
        if not self.validation_users_check:
            raise ValidationError(
                'La validación no ha sido aprobada por los usuarios asignados')
        self.cancel_other_versions()
        self.write({
            'state': 'validate_ok',
        })
        validate_activity = self.activity_ids.filtered(
            lambda r: r.summary == 'Validación de documento')
        for validate in validate_activity:
            validate.action_done()
        self.write({})
        self.notify_to_users()
        change_message = ''
        diff = ''
        related_fields = ['purpose', 'scope', 'references', 'body', 'flowchart',
                          'abbreviation_ids', 'responsable_ids', 'documentarycontrol_ids']
        if not self.old_versions:
            change_message += 'Versión Inicial'
            self.env['process.edition.history'].create({
                'name': change_message,
                'numero': self.numero,
                'process_edition_id': self.id,
                'publish_date': fields.Date.today(),
            })
        else:
            prev = self.old_versions[-1] if self.old_versions else None
            for other in self.old_versions:
                other.send_cancel()
            for field in related_fields:
                if prev:
                    diff = self.getDiff(prev.id, self.id, field)
                else:
                    diff = self.getDiff(False, self.id, field)
                change_message += diff
            self.env['process.edition.history'].create({
                'name': change_message,
                'numero': self.numero,
                'process_edition_id': self.id,
                'publish_date': self.date_validate,
            })

    @api.model
    def getDiff(self, v1, v2, field):
        """Return the difference between two version of document version."""
        text1 = v1 and getattr(self.browse(v1), field) or ''
        text2 = v2 and getattr(self.browse(v2), field) or ''
        if text1 == text2:
            return ''
        else:
            return 'Campo %s actualizado\n' % self._fields[field].string


class MgmtCateg(models.Model):
    _inherit = 'mgmt.categ'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmt_categ_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmt_categ_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmt_categ_validation_id', string='Validación')
    
    parent_edition = fields.Many2one(
        comodel_name='mgmt.categ', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmt.categ', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def _copy_edition(self):
        new_edition = self.copy({
            'version': self.version,
            'deactivate_date': fields.Date.today(),
            'parent_edition': self.id,
        })
        return new_edition

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_process.action_mgmt_categ_procedures').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def button_new_version(self):
        self.ensure_one()
        self._copy_edition()
        revno = self.version
        self.write({
            'version': revno + 1,
            'name': self.name
        })


class ProcessEditionValidationStep(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    process_edition_elaboration_id = fields.Many2one(
        'process.edition', string='Edición de procedimiento (Elaboración)')
    process_edition_review_id = fields.Many2one(
        'process.edition', string='Edición de procedimiento (Revisión)')
    process_edition_validation_id = fields.Many2one(
        'process.edition', string='Edición de procedimiento (Validación)')

    mgmt_categ_elaboration_id = fields.Many2one(
        'mgmt.categ', string='Proceso (Elaboración)')
    mgmt_categ_review_id = fields.Many2one(
        'mgmt.categ', string='Proceso (Revisión)')
    mgmt_categ_validation_id = fields.Many2one(
        'mgmt.categ', string='Proceso (Validación)')
