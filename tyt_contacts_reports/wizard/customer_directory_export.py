from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CustomerDirectory(models.TransientModel):
    _name = 'customer_directory.export'
    _description = 'Customer Directory Export'

    customer_directory_ids = fields.Many2many(
        comodel_name='customer_directory',
        relation='customer_directory_export_rel',  # Manually specify a shorter relation table name
        column1='wizard_id',  # Name for the first column in the relation table
        column2='model_id',  # Name for the second column in the relation table
        string='Customer Directory'
    )

    def export_xlsx_report(self):
        data = {}
        return (self.env.ref('tyt_contacts_reports.customer_directory_xlsx_report_action').
                report_action(self.customer_directory_ids, data=data))
