from odoo import api, fields, models, _


class SupplierComplaintsInventory(models.Model):
    _name = 'supplier_complaints_inventory'
    _description = 'Supplier Complaints Inventory'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'supplier_id'

    shipment_date = fields.Date(string='Shipment Date', tracking=True)
    product_service = fields.Text(string='Product/Service', tracking=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', tracking=True)
    description = fields.Text(string='Description', tracking=True)
    document_reference = fields.Text(string='Document Reference', tracking=True)
    resolution_date = fields.Date(string='Resolution Date', tracking=True)
    register_id = fields.Many2one('res.users', string='Registered By', tracking=True)
