from odoo import api, fields, models, _


class Mailbox(models.Model):
    _name = 'tyt.intranet.mailbox'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Mailbox'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    user_id = fields.Many2one('res.users', string='User')
    partner_id = fields.Many2one('res.partner', related='user_id.partner_id', string='Partner')
    partner_email = fields.Char(related='partner_id.email', string='Partner Email')
    employee_number = fields.Char(related='user_id.x_studio_numero', string='Employee Number', store=True)
    is_anonymous = fields.Boolean(string='Is Anonymous')
    site_id = fields.Many2one('x_sitios', string='Site')
    service_area_id = fields.Many2one('tyt.intranet.service_area', string='Service Area')
    message_type_id = fields.Many2one('tyt.intranet.message_type', string='Message Type')
    receive_response = fields.Boolean(string='Receive Response')
    comment = fields.Html(string='Comment')
    response_message = fields.Html(string='Response Message', compute='_compute_response_message', store=True, readonly=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    state = fields.Selection([
        ('received', 'Received'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated')], string='State', default='received', tracking=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Urgent')], string='Priority', tracking=True)
    responsible_id = fields.Many2one('res.users', string='Responsible', domain="[('share', '=', False)]", tracking=True)
    deadline_date = fields.Date(string='Deadline Date', tracking=True)
    close_date = fields.Date(string='Close Date', tracking=True)
    response = fields.Html(string='Response')
    survey_id = fields.Many2one('survey.survey', string='Survey', domain="[('access_mode', '=', 'public')]")
    matrix_id = fields.Many2one('tyt.intranet.notification_matrix', compute='_compute_matrix_id', string='Matrix')
    responsible_ids = fields.Many2many('res.users', compute='_compute_responsible_ids', string='Responsibles')

    @api.depends('matrix_id', 'matrix_id.matrix_line_ids')
    def _compute_responsible_ids(self):
        for record in self:
            responsible_users = self.env['res.users']
            if record.matrix_id and record.service_area_id and record.message_type_id:
                matrix_lines = record.matrix_id.matrix_line_ids.filtered(
                    lambda line: line.service_area_id == record.service_area_id
                )
                matrix_line_message_types = matrix_lines.mapped('matrix_line_message_type_ids').filtered(
                    lambda mt: mt.message_type_id == record.message_type_id
                )
                for matrix_line_message_type in matrix_line_message_types:
                    responsible_users |= matrix_line_message_type.user_ids
                for matrix_line in matrix_lines:
                    if matrix_line.responsible_id:
                        responsible_users |= matrix_line.responsible_id
            record.responsible_ids = [(6, 0, responsible_users.ids)]

    @api.depends('site_id')
    def _compute_matrix_id(self):
        for record in self:
            record.matrix_id = self.env['tyt.intranet.notification_matrix'].search([
                ('site_id', '=', record.site_id.id),
            ], order='create_date desc', limit=1)

    @api.depends('message_type_id', 'close_date', 'response', 'survey_id')
    def _compute_response_message(self):
        for record in self:
            message_type = record.message_type_id.name or 'Mensaje'
            close_date = record.close_date.strftime('%d/%m/%Y') if record.close_date else ''
            response = record.response or ''

            if record.survey_id:
                survey_url = f"/survey/start/{record.survey_id.access_token}"
                survey_message = f"""<p><strong>Encuesta de satisfacción: </strong>
                                     <a href="{survey_url}" target="_blank">{record.survey_id.title}</a></p>"""
            else:
                survey_message = ''

            record.response_message = f"""
                <p>Hemos recibido tu {message_type} y estamos trabajando en resolverla.</p>
                <p><strong>Fecha de cierre: </strong>{close_date}</p>
                <p><strong>Respuesta final: </strong>{response}</p>
                {survey_message}
            """

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_resolved(self):
        self.write({'state': 'resolved'})

    def action_escalated(self):
        self.write({'state': 'escalated'})

    @api.depends('message_type_id')
    def _compute_name(self):
        for record in self:
            if record.message_type_id:
                record.name = f'{record.message_type_id.name}'
            else:
                record.name = ''

    def get_emails_to_send(self):
        self.ensure_one()
        return ', '.join(self.responsible_ids.mapped('email'))

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
