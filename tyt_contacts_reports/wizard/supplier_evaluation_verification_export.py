from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SupplierEvaluationVerification(models.TransientModel):
    _name = 'supplier_evaluation_verification.export'
    _description = 'Supplier Evaluation Verification Export'

    def export_xlsx_report(self):
        data = {}
        return self.env.ref('tyt_contacts_reports.supplier_evaluation_verification_xlsx_report_action').report_action(self, data=data)
