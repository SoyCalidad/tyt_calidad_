from odoo import api, fields, models

class SupplierWizard(models.TransientModel):
    _name = 'supplier.wizard.report'

    is_critical = fields.Boolean(string='Solo proveedores críticos')
    
    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'critical': self.is_critical,
            'model': 'supplier.wizard.report',
            'res_model': 'supplier.wizard.report',
        }
        return self.env.ref('mgmtsystem_process_integration.action_report_suppliers').report_action(self, data=datas)
    
class CustomerWizard(models.TransientModel):
    _name = 'customer.wizard.report'

    is_critical = fields.Boolean(string='Solo clientes críticos')
    
    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'critical': self.is_critical,
            'model': 'customer.wizard.report',
            'res_model': 'customer.wizard.report',
        }
        return self.env.ref('mgmtsystem_process_integration.action_report_customers').report_action(self, data=datas)