from odoo import api, fields, models, _


class SupplierComplaintsInventory(models.TransientModel):
    _name = 'supplier_complaints_inventory.export'
    _description = 'Supplier Complaints Inventory Export'

    date_from = fields.Date(string='Shipment Date From')
    date_to = fields.Date(string='Shipment Date To')

    def export_xlsx_report(self):
        data = {
            'is_wizard': True,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return self.env.ref('tyt_contacts_reports.supplier_complaint_inventory_xlsx_report_action').report_action(self, data=data)
