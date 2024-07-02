from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import base64
import tempfile


class ComunicationPlan(models.Model):
    _inherit = 'comunication.plan'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'comunication_plan_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'comunication_plan_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'comunication_plan_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    parent_edition = fields.Many2one(
        comodel_name='comunication.plan', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='comunication.plan', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_comunication.comunication_plan_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def send_elaborate(self):
        super().send_elaborate()
        self.create_child_validation_users(self.line_ids)
        for audit in self.line_ids:
            try:
                audit.send_elaborate()
            except:
                pass

    def send_review(self):
        super().send_review()
        self.create_child_validation_users(self.line_ids)
        for audit in self.line_ids:
            try:
                audit.send_review(notify=False)
            except:
                pass

    def send_validate(self):
        super().send_validate()
        self.create_child_validation_users(self.line_ids)
        for audit in self.line_ids:
            try:
                audit.send_validate(notify=False)
            except:
                pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.create_child_validation_users(self.line_ids)
        for audit in self.line_ids:
            audit.send_validate_ok()

    def send_cancel(self):
        super().send_cancel()
        for audit in self.line_ids:
            try:
                audit.send_cancel()
            except:
                pass

    def action_notify_employee(self):
        for each in self:
            for line in each.line_ids:
                line.action_notify_employee()

    def notify_email_odoo(self):
        for each in self:
            for line in each.line_ids:
                line.notify_email_odoo()


class ComunicationPlanLine(models.Model):
    _inherit = 'comunication.plan.line'

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('on_track', 'En seguimiento'),
            ('closed', 'Terminado'),
            ('cancel', 'Obsoleto'),
        ],
        default='elaborate',
        copy=False,
    )

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'comunication_plan_line_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'comunication_plan_line_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'comunication_plan_line_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    parent_edition = fields.Many2one(
        comodel_name='comunication.plan.line', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='comunication.plan.line', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_comunication.plan_line_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def action_notify_employee(self):
        for each in self:
            notification_ids = []
            try:
                date = each.date_release.strftime('%d/%m/%Y')
                body = "Plan de comunicación pendiente: " + each.resume + ' el ' + date
                for partner in each.partner_ids:
                    notification_ids.append((0, 0, {
                        'res_partner_id': partner.id,
                        'notification_type': 'inbox'}))
                self.message_post(body=body, message_type='notification',
                                  subtype='mail.mt_comment', author_id=2, notification_ids=notification_ids)
            except:
                pass

    def action_notify_comunication_plan(self):
        self.ensure_one()
        template = 'mgmtsystem_comunication.email_template_comunication_plan_line'
        return self.notify_users_by_email(template)

    def notify_email_odoo(self):
        self.ensure_one()
        sender = self.env.company.email
        for each in self.employee_ids:
            date = self.date_release.strftime('%d/%m/%Y')
            body = 'Le hago llegar el plan de comunicaciones  %s' % self.name
            fp = tempfile.NamedTemporaryFile(suffix='.pdf')
            data, data_format = self.env.ref(
                'mgmtsystem_comunication.action_report_comunication_plan_line').render([self.id])
            fp.write(data)
            part = open(fp.name, 'rb').read()
            attachment = self.env['ir.attachment'].create({
                'datas': base64.b64encode(part),
                'name': 'Comunicación.pdf'})
            template_data = {
                'subject':  "Comunicación %s" % date,
                'body_html': body,
                'email_from': sender,
                'email_to': each.work_email,
                'attachment_ids': [(4, attachment.id)]
            }
            self.env['mail.mail'].create(template_data).send()


class ComunicationPlanValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    comunication_plan_elaboration_id = fields.Many2one(
        'comunication.plan', string='Padre (Elaboración de programa de comunicación)')
    comunication_plan_review_id = fields.Many2one(
        'comunication.plan', string='Padre (Revisión de programa de comunicación)')
    comunication_plan_validation_id = fields.Many2one(
        'comunication.plan', string='Padre (Validación de programa de comunicación)')

    comunication_plan_line_elaboration_id = fields.Many2one(
        'comunication.plan.line', string='Padre (Elaboración de plan de comunicación)')
    comunication_plan_line_review_id = fields.Many2one(
        'comunication.plan.line', string='Padre (Revisión de plan de comunicación)')
    comunication_plan_line_validation_id = fields.Many2one(
        'comunication.plan.line', string='Padre (Validación de plan de comunicación)')
