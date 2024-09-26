from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CustomerProperty(models.Model):
    _name = 'customer_property'
    _description = 'Customer Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

