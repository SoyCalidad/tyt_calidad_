from odoo import api, fields, models, _


class Mailbox(models.Model):
    _name = 'tyt.intranet.mailbox'
    _description = 'Mailbox'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    user_id = fields.Many2one('res.users', string='User')
    partner_id = fields.Many2one('res.partner', string='Partner')
    employee_number = fields.Char(string='Employee Number')


    email = fields.Char(string='Email')

    is_anonymous = fields.Boolean(string='Is Anonymous')
    site_id = fields.Many2one('x_sitios', string='Site')
    service_area_id = fields.Many2one('tyt.intranet.service_area', string='Service Area')
    message_type_id = fields.Many2one('tyt.intranet.message_type', string='Message Type')
    comment = fields.Html(string='Comment')
    users_to_send = fields.Many2many('res.users', string='Users to Send')
    emails_string = fields.Char(string='Email List')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    receive_response = fields.Boolean(string='Receive Response')
    response_message = fields.Text(string='Response Message')


    def get_emails_to_send(self):
        self.ensure_one()
        # Ensure that the required fields are set
        if not self.site_id or not self.service_area_id or not self.message_type_id:
            return ""

        # Step 1: Find the Notification Matrix Line based on the site and service area
        matrix_lines = self.env['tyt.intranet.notification_matrix.line'].search([
            ('notification_matrix_id.site_id', '=', self.site_id.id),
            ('service_area_id', '=', self.service_area_id.id)
        ])

        if not matrix_lines:
            return ""

        # Step 2: Find the Notification Matrix Line Message Type based on the message_type_id
        matrix_line_message_types = self.env['tyt.intranet.notification_matrix.line.message_type'].search([
            ('notification_matrix_line_id', 'in', matrix_lines.ids),
            ('message_type_id', '=', self.message_type_id.id)
        ])

        if not matrix_line_message_types:
            return ""

        # Step 3: Collect emails for the specific message type
        user_emails = []
        for matrix_line_message_type in matrix_line_message_types:
            user_emails.extend(matrix_line_message_type.user_ids.mapped('email'))

        # Step 4: Add responsible user's email to the list (if exists)
        for matrix_line in matrix_lines:
            if matrix_line.responsible_id and matrix_line.responsible_id.email:
                user_emails.append(matrix_line.responsible_id.email)

        # Remove duplicates and create a comma-separated string
        unique_emails = list(set(user_emails))
        emails_string = ','.join(unique_emails)

        # Store the result in the 'emails_string' field
        self.emails_string = emails_string

        return emails_string

    def send_mail(self):
        self.ensure_one()
        template = self.env.ref('tyt_intranet_helpdesk.mail_template_tyt_intranet_mailbox', raise_if_not_found=False)
        #self.notify_users_by_email(self.id, template_name)

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
