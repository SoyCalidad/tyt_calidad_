from odoo import api, fields, models, _
from odoo.exceptions import UserError
from random import randint


class DepartmentMessageTag(models.Model):
    _name = 'tyt.intranet.department_message.tag'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Name')
    color = fields.Integer(string='Color', default=_get_default_color)
    active = fields.Boolean(string='Active', default=True)


class DepartmentMessage(models.Model):
    _name = 'tyt.intranet.department_message'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Department Message'
    _rec_name = 'subject'

    subject = fields.Char(string='Subject')
    body = fields.Html(string='Body')
    footer = fields.Html(string='Footer')

    sender_id = fields.Many2one('res.users', string='Sender', default=lambda self: self.env.user)
    website_id = fields.Many2one('website', string='Website')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    deadline_date = fields.Date(string='Deadline Date')
    tag_ids = fields.Many2many('tyt.intranet.department_message.tag', string='Tags')
