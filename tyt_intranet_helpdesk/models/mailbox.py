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
    comment = fields.Html(string='Comment')
