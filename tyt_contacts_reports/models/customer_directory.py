from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CustomerDirectory(models.Model):
    _name = 'customer_directory'
    _description = 'Customer Directory'
    _inherit = ['mail.thread', 'mail.activity.mixin']

