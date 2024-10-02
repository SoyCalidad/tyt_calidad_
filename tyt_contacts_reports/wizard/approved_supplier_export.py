from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ApprovedSupplier(models.TransientModel):
    _name = 'approved_supplier.export'
    _description = 'Approved Supplier Export'

    is_critical = fields.Boolean(string='Critical Supplier', default=False)

    def export_xlsx_report(self):
        data = {
            'is_wizard': True,
            'is_critical': self.is_critical,
        }
        return self.env.ref('tyt_contacts_reports.approved_supplier_xlsx_report_action').report_action(self, data=data)
