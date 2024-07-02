

"""Clase principal para el envío de correo electrónico y notificaciones para los distintos modelos."""
from operator import mod

from odoo import api, fields, models


class EmailBasic(models.AbstractModel):
    """Clase básica que gestiona los envíos de correos electrónicos."""
    _name = 'iso_base.email_basic'
    _description = 'Gestión básica de envío de correos electrónicos'

    def notify_users_by_email(self, template, fast=False):
        """Envía un correo electrónico a los usuarios relacionados para notificarles.

        Args:
            template (string): Nombre del template de correo electrónico.
            fast (bool, optional): Usarse en caso se desee envíar el correo electrónico sin la 
            ventana emergente. Defaults to False.

        """
        template = self.env.ref(template, raise_if_not_found=True)
        model = self._name

        # Envia el correo electrónico de manera inmediata sin la ventana emergente
        if fast:
            self.env['mail.template'].browse(
                template.id).send_mail(self.id, force_send=True, notif_layout="mail.mail_notification_light",)
            return True

        else:
            if template.lang:
                lang = template._render_template(
                    template.lang, model, self.ids[0])
            else:
                lang = self.env.user.lang

            ctx = {
                'default_model': model,
                'default_res_id': self.ids[0],
                'default_use_template': bool(template),
                'default_template_id': template.id,
                'default_composition_mode': 'comment',
                'mark_so_as_sent': True,
                'custom_layout': "mail.mail_notification_light",
                'force_email': True,
                'model_description': self.with_context(lang=lang).name,
            }
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(False, 'form')],
                'view_id': False,
                'target': 'new',
                'context': ctx,
            }

    def notify_users_by_system(self, partners, body):
        notification_ids = []
        for partner in partners:
            notification_ids = []
            notification_ids.append((0, 0, {
                'res_partner_id': partner.id,
                'notification_type': 'inbox'}))
        self.message_post(body=body, message_type='notification',
                          subtype_id=self.env.ref('mail.mt_comment').id, author_id=2, notification_ids=notification_ids)
                        # to Odoo 15's compatibility, change subtype='mail.mt_comment' --> subtype_id=self.env.ref('mail.mt_comment').id
    def notify_users_by_activity(self, user, body):
        self.env.cr.execute("""SELECT id FROM ir_model 
                            WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        todo_id = self.env['mail.activity.type'].search(
            [('name', '=', 'To Do')], limit=1).id
        self.env['mail.activity'].sudo().create({
            'res_id': self.ids[0],
            'res_model_id': model_id,
            'res_model': self._name,
            'summary': body,
            'user_id': user.id,
            'activity_type_id': int(todo_id),
        })
