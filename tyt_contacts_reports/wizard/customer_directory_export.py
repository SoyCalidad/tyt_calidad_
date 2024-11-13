from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CustomerDirectory(models.TransientModel):
    _name = 'customer_directory.export'
    _description = 'Customer Directory Export'

    is_critical = fields.Boolean(string='Critical Customer', default=False)

    def export_xlsx_report(self):
        data = {
            'is_wizard': True,
            'is_critical': self.is_critical,
        }
        return self.env.ref('tyt_contacts_reports.customer_directory_xlsx_report_action').report_action(self, data=data)
