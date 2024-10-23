from odoo import api, fields, models, _


class Mailbox(models.Model):
    _name = 'tyt.intranet.mailbox'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Mailbox'

    name = fields.Char(string='Title', compute='_compute_name', store=True)
    user_id = fields.Many2one('res.users', string='User')
    partner_id = fields.Many2one('res.partner', related='user_id.partner_id', string='Partner')
    partner_name = fields.Char(string='Partner Name')
    partner_email = fields.Char(string='Partner Email')
    employee_number = fields.Char(string='Employee Number')
    is_anonymous = fields.Boolean(string='Is Anonymous')
    site_id = fields.Many2one('x_sitios', string='Site')
    service_area_id = fields.Many2one('tyt.intranet.service_area', string='Service Area')
    message_type_id = fields.Many2one('tyt.intranet.message_type', string='Message Type')
    receive_response = fields.Boolean(string='Receive Response')
    comment = fields.Html(string='Comment')
    response_message = fields.Html(string='Response Message')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.depends('message_type_id')
    def _compute_name(self):
        for record in self:
            if record.message_type_id:
                record.name = f'{record.message_type_id.name}'
            else:
                record.name = ''

    def get_emails_to_send(self):
        self.ensure_one()
        if not self.site_id or not self.service_area_id or not self.message_type_id:
            return ''
        matrix_lines = self.env['tyt.intranet.notification_matrix.line'].search([
            ('notification_matrix_id.site_id', '=', self.site_id.id),
            ('service_area_id', '=', self.service_area_id.id)
        ])
        if not matrix_lines:
            return ''
        matrix_line_message_types = self.env['tyt.intranet.notification_matrix.line.message_type'].search([
            ('notification_matrix_line_id', 'in', matrix_lines.ids),
            ('message_type_id', '=', self.message_type_id.id)
        ])
        if not matrix_line_message_types:
            return ''
        user_emails = []
        for matrix_line_message_type in matrix_line_message_types:
            user_emails.extend(matrix_line_message_type.user_ids.mapped('email'))
        for matrix_line in matrix_lines:
            if matrix_line.responsible_id and matrix_line.responsible_id.email:
                user_emails.append(matrix_line.responsible_id.email)
        unique_emails = list(set(user_emails))
        emails_string = ','.join(unique_emails)
        return emails_string

    def send_mail_modal(self):
        self.ensure_one()
        template = self.env.ref('tyt_intranet_helpdesk.mail_template_tyt_intranet_mailbox', raise_if_not_found=False)
        lang = self.env.context.get('lang')
        ctx = {
            'default_model': self._name,
            'default_res_id': self.ids[0],
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': 'mail.mail_notification_light',
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

    def send_mail(self):
        self.ensure_one()
        template = self.env.ref('tyt_intranet_helpdesk.mail_template_tyt_intranet_mailbox', raise_if_not_found=False)
        template.send_mail(self.id, force_send=True)
