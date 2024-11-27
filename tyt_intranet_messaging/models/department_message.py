from odoo import api, fields, models, _
from odoo.exceptions import UserError
from random import randint


class DepartmentMessageTag(models.Model):
    _name = 'tyt.intranet.department_message.tag'
    _description = 'Department Message Tag'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Name')
    color = fields.Integer(string='Color', default=_get_default_color)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Tag name already exists!'),
    ]


class DepartmentMessageReadStatus(models.Model):
    _name = 'tyt.intranet.department_message.read_status'
    _description = 'Department Message Read Status'

    department_message_id = fields.Many2one('tyt.intranet.department_message', string='Department Message')
    user_id = fields.Many2one('res.users', string='User')
    is_read = fields.Boolean(string='Is Read', default=False, tracking=True)


class DepartmentMessage(models.Model):
    _name = 'tyt.intranet.department_message'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Department Message'
    _rec_name = 'sender_portal'

    is_read = fields.Boolean(string='Is Read', default=False)

    sender_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user, domain="[('share', '=', False)]")
    sender_char = fields.Char(string='Sender')
    sender_portal = fields.Char(string='Sender Portal', compute='_compute_sender_portal', store=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', copy=False)

    published_date = fields.Date(string='Published Date', copy=False, default=fields.Date.today)
    deadline_date = fields.Date(string='Deadline Date', copy=False)
    tag_ids = fields.Many2many('tyt.intranet.department_message.tag', 'tyt_intranet_department_message_tag_rel',
                               'message_id', 'tag_id', string='Tags')

    subject = fields.Text(string='Subject')
    body = fields.Html(string='Body')
    footer = fields.Html(string='Footer')

    job_id = fields.Many2one('hr.job', string='Job Position')
    department_id = fields.Many2one('hr.department', string='Department')
    gps = fields.Boolean(string='gps')
    group_ids = fields.Many2many('res.groups', 'tyt_intranet_department_message_group_rel',
                                 'message_id', 'group_id', string="Groups")

    read_status_ids = fields.One2many('tyt.intranet.department_message.read_status', 'department_message_id', string='Read Status')

    @api.onchange('gps')
    def onchange_gps(self):
        self.ensure_one()
        if self.gps and self.job_id:
            groups = self.env['res.groups'].search([('x_studio_job', '=', self.job_id.id)])
            self.group_ids = [(6, 0, [groups.id])] if groups else []
            existing_user_ids = self.read_status_ids.mapped('user_id.id')
            new_user_ids = groups.mapped('users.id')
            unique_user_ids = set(new_user_ids) - set(existing_user_ids)
            read_status_vals = [{'user_id': user_id, 'department_message_id': self.id} for user_id in unique_user_ids]
            self.read_status_ids = [(0, 0, vals) for vals in read_status_vals]
            self.gps = False

    def is_read_by_current_user(self):
        """Check if the current user has read this message."""
        self.ensure_one()  # Ensure we're working with a single record
        current_user = self.env.user
        # Find the user's read status record
        read_record = self.read_status_ids.filtered(lambda r: r.user_id == current_user)
        print('#################')
        print(read_record.is_read)
        return read_record.is_read if read_record else False

    def mark_as_read_by_current_user(self):
        print('#################')
        self.ensure_one()
        current_user = self.env.user
        print(current_user)
        department_message = self.read_status_ids.filtered(lambda r: r.user_id == current_user)
        print(department_message)
        if department_message:
            print('################# If')
            print(department_message)
            department_message.is_read = True


    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
    ], string='State', default='draft')

    website_id = fields.Many2one('website', string='Website')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.depends('sender_char', 'sender_id')
    def _compute_sender_portal(self):
        for record in self:
            if record.sender_char:
                record.sender_portal = record.sender_char
            else:
                record.sender_portal = record.sender_id.name

    def action_draft(self):
        self.ensure_one()
        self.state = 'draft'

    def action_publish(self):
        self.ensure_one()
        self.state = 'published'
        Attachment = self.env['ir.attachment']
        for attachment in self.attachment_ids:
            attachment.write({'access_token': Attachment._generate_access_token()})
