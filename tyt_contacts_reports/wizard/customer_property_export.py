from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CustomerProperty(models.TransientModel):
    _name = 'customer_property.export'
    _description = 'Customer Property Export'

    def export_xlsx_report(self):
        data = {}
        return self.env.ref('tyt_contacts_reports.customer_property_xlsx_report_action').report_action(self, data=data)
