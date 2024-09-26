from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ApprovedSupplier(models.TransientModel):
    _name = 'approved_supplier.export'
    _description = 'Approved Supplier Export'

    def export_xlsx_report(self):
        data = {}
        return self.env.ref('tyt_contacts_reports.approved_supplier_xlsx_report_action').report_action(self, data=data)
