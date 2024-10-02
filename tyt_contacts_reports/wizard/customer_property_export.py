from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CustomerProperty(models.TransientModel):
    _name = 'customer_property.export'
    _description = 'Customer Property Export'

    is_critical = fields.Boolean(string='Critical Customer', default=False)

    def export_xlsx_report(self):
        data = {
            'is_wizard': True,
            'is_critical': self.is_critical,
        }
        return self.env.ref('tyt_contacts_reports.customer_property_xlsx_report_action').report_action(self, data=data)
