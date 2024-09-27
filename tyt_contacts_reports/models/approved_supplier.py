from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ApprovedSupplier(models.Model):
    _name = 'approved_supplier'
    _description = 'Approved Supplier'
    _inherit = ['mail.thread', 'mail.activity.mixin']

