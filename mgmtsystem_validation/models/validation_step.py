from odoo.exceptions import ValidationError
from odoo import _, api, fields, models
import logging


_logger = logging.getLogger(__name__)


class ValidationStep(models.Model):
    _name = 'mgmtsystem.validation.step'
    _description = 'Etapas de validación'
    _rec_name = 'user_id'

    user_id = fields.Many2one('res.users', string='Usuario', required=True)
    date = fields.Datetime(string='Fecha', default=fields.Datetime.now())
    check = fields.Boolean(string='Efectuado')

    validation_elaboration_id = fields.Many2one(
        'mgmtsystem.validation.mail', string='Elaboración')
    validation_review_id = fields.Many2one(
        'mgmtsystem.validation.mail', string='Revisión')
    validation_validation_id = fields.Many2one(
        'mgmtsystem.validation.mail', string='Validación')

    current_user_can_validate = fields.Boolean(
        compute='_get_current_user_can_validate', string='Usuario actual está autorizado para aprobar')

    @api.depends('user_id')
    def _get_current_user_can_validate(self):
        current_user = self.env.user
        for each in self:
            if each.user_id.id == current_user.id:
                each.current_user_can_validate = True
            else:
                each.current_user_can_validate = False


class Validation(models.Model):
    _name = 'mgmtsystem.validation'
    _description = 'Validación del sistema de gestión'
    _inherit = 'mgmtsystem.version'

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('cancel', 'Obsoleto')
        ],
        default='elaborate',
        copy=False,
        tracking=True
    )

    def write(self, values):
        result = super(Validation, self).write(values)
        return result

    def cancel_other_versions(self):
        """Cancela las versiones anteriores"""
        for each in self:
            for version in each.old_versions:
                version.write({
                    'state': 'cancel'
                })

    ###############################################################################
    ############# Sobreescribir en cada modelo que se requiera usar ###############

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'validation_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'validation_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'validation_validation_id', string='Validación')

    ###############################################################################

    elaboration_users_check = fields.Boolean(
        compute='_get_users_check', string='Aprobada elaboración')
    review_users_check = fields.Boolean(
        compute='_get_users_check', string='Aprobada revisión')
    validation_users_check = fields.Boolean(
        compute='_get_users_check', string='Aprobada validación')

    date_elaborate = fields.Date(
        string='Fecha de elaboración', default=fields.Date.today(), tracking=True)
    date_review = fields.Date(
        string='Fecha de revisión', tracking=True)
    date_validate = fields.Date(
        string='Fecha de validación', tracking=True)

    last_validate_date = fields.Date(
        compute='_compute_last_validate_date', string='Última fecha de validación')

    @api.depends('date_validate')
    def _compute_last_validate_date(self):
        for record in self:
            date_validate = None
            dates = [x.date for x in record.validation_step]
            if dates:
                date_validate = max(dates)
            record.last_validate_date = date_validate

    def _get_users_check(self):
        def false_if_not_checked(records):
            for record in records:
                if not record.check:
                    return False
            return True
        self.elaboration_users_check = false_if_not_checked(
            self.elaboration_step) if self.elaboration_step else False
        self.review_users_check = false_if_not_checked(
            self.review_step) if self.review_step else False
        self.validation_users_check = false_if_not_checked(
            self.validation_step) if self.validation_step else False
        

    def get_step_user_list(self, step):
        """Devuelve una lista de texto de usuarios asignados a una etapa de aprobación"""
        user_list = '\n'
        for line in step:
            if not line.check:
                user_list += '\t- {}\n'.format(line.user_id.name)
        return user_list

    def send_elaborate(self):
        if not self.elaboration_step:
            raise ValidationError('Ingrese los usuarios para la Elaboración')
        self.write({'state': 'elaborate'})
        self.notify_to_step_users(self.elaboration_step, 'elaboration')

    def send_review(self, notify=True):
        if not self.review_step:
            raise ValidationError('Ingrese los usuarios para la Revisión')
        if not self.elaboration_users_check:
            user_list = self.get_step_user_list(self.elaboration_step)
            raise ValidationError(
                'La elaboración no ha sido aprobada por {}'.format(user_list))
        self.write({
            'state': 'review',
            'date_review': fields.Date.today()
        })
        if notify:
            self.notify_to_step_users(self.review_step, 'review')

    def send_validate(self, notify=True):
        if not self.validation_step:
            raise ValidationError('Ingrese los usuarios para la validación')
        if not self.review_users_check:
            user_list = self.get_step_user_list(self.review_step)
            raise ValidationError(
                'La revisión no ha sido aprobada por {}'.format(user_list))
        self.write({
            'state': 'validate',
        })
        if notify:
            self.notify_to_step_users(self.validation_step, 'validation')

        review_activity = self.activity_ids.filtered(
            lambda r: r.summary == 'Revisión de documento')
        for review in review_activity:
            review.action_done()

    def send_validate_ok(self):
        if not self.validation_users_check:
            user_list = self.get_step_user_list(self.validation_step)
            raise ValidationError(
                'La validación no ha sido aprobada por {}'.format(user_list))
        self.cancel_other_versions()
        date_validate = None
        dates = [x.date for x in self.validation_step]
        if dates:
            date_validate = max(dates)
        validate_activity = self.activity_ids.filtered(
            lambda r: r.summary == 'Validación de documento')
        for validate in validate_activity:
            validate.action_done()
        self.write({
            'state': 'validate_ok',
            'date_validate': date_validate,
        })

    def send_cancel(self):
        self.write({'state': 'cancel'})

    def notify_to_step_users(self, steps, type):
        body = ''
        self.env.cr.execute("""SELECT id FROM ir_model 
                            WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        if type == 'elaboration':
            body += 'Elaboración de documento'
        elif type == 'review':
            body += 'Revisión de documento'
        elif type == 'validation':
            body += 'Validación de documento'
        for step in steps:
            name = self.name or ''
            if step.user_id:
                todo_id = self.env['mail.activity.type'].search(
                    [('name', '=', 'To Do')], limit=1).id
                self.env['mail.activity'].create({
                    'res_id': self.ids[0],
                    'res_model_id': model_id,
                    'res_model': self._name,
                    'summary': body,
                    'user_id': step.user_id.id,
                    'activity_type_id': int(todo_id),
                })

    def create_activity(self, steps, type):
        body = ''
        if type == 'elaboration':
            body += 'Elaboración de documento'
        elif type == 'review':
            body += 'Revisión de documento'
        elif type == 'validation':
            body += 'Validación de documento'
        notification_ids = []
        for step in steps:
            notification_ids.append((0, 0, {
                'res_partner_id': step.user_id.partner_id.id,
                'notification_type': 'inbox'}))
        self.message_post(body=body, message_type='notification',
                          subtype='mail.mt_comment', author_id=2, notification_ids=notification_ids)

    # Version inherit

    def remove_validation_steps_users(self):
        """Remove the items from the steps in a new version"""
        for each in self:
            for item in each.elaboration_step + each.review_step + each.validation_step:
                item.unlink()

    def _copy_edition(self):
        fields_to_copy = ['elaboration_step', 'review_step', 'validation_step']
        copy_data_dict = {
            'deactivate_date': fields.Date.today(),
            'parent_edition': self.id,
            'version': self.version,
            'state': self.state,
        }
        for field in fields_to_copy:
            if field in self._fields:
                copy_data_dict[field] = [(6, 0, getattr(self, field).ids)]
        new_edition = self.copy(copy_data_dict)

        return new_edition

    def button_new_version(self):
        """Copia los datos base de la edición anterior"""

        self.ensure_one()
        old_edition = self._copy_edition()
        revno = self.version
        self.write({
            'version': revno + 1,
            'state': 'elaborate',
            'name': self.name
        })
        child_fields = ['audit_ids', 'line_ids',
                        'training_ids', 'maintenance_ids']

        for field in child_fields:
            if hasattr(self, field):
                lines = getattr(self, field)
                old_childs = self.clone_childs(lines)
                old_edition.write({field: [(6, 0, old_childs)]})

    def clone_childs(self, childs):
        old_ids = []
        for child in childs:
            old_child = child._copy_edition()
            old_ids.append(old_child.id)
        for child in childs:
            child.state = 'elaborate'

        return old_ids

    def create_child_validation_users(self, childs):
        for m in childs:
            if m.elaboration_step:
                for record in m.elaboration_step:
                    record.check = True
            if m.review_step:
                for record in m.review_step:
                    record.check = True
            if m.validation_step:
                for record in m.validation_step:
                    record.check = True
            
            if not m.elaboration_step and self.elaboration_step:
                m.elaboration_step = [(0, 0, {
                    'user_id': x.user_id.id,
                    'check': True,
                    'date': x.date,
                }) for x in self.elaboration_step]
            if not m.review_step and self.review_step:
                m.review_step = [(0, 0, {
                    'user_id': x.user_id.id,
                    'check': True,
                    'date': x.date,
                }) for x in self.review_step]
            if not m.validation_step and self.validation_step:
                m.validation_step = [(0, 0, {
                    'user_id': x.user_id.id,
                    'check': True,
                    'date': x.date,
                }) for x in self.validation_step]

class MailValidation(models.Model):
    _name = 'mgmtsystem.validation.mail'
    _inherit = ['mgmtsystem.validation', 'mail.thread', 'mail.activity.mixin']
    _description = 'Comunicación de validación'
