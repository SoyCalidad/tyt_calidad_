from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SupplierEvaluationVerification(models.Model):
    _name = 'supplier_evaluation_verification'
    _description = 'Supplier Evaluation Verification'
    _inherit = ['mail.thread', 'mail.activity.mixin']
