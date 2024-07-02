from odoo import api, fields, models


class SupplierReport(models.AbstractModel):
    _name = 'report.mgmtsystem_process_integration.supplier_report'
    _inherit = 'mgmtsystem.code'
    _description = 'Listado de proveedores y proveedores críticos'

    @api.model
    def _get_report_values(self, docids, data=None):
        critical = False
        if data.get('critical'):
            suppliers = self.env['res.partner'].search(
                [('supplier', '=', 1), ('vip_supplier', '=', 1)])
            critical = True
        else:
            suppliers = self.env['res.partner'].search([('supplier', '=', 1)])
        suppliers_info = self.env['product.supplierinfo'].search(
            [('name', 'in', [x.id for x in suppliers])])

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'critical': critical,
            'docs': [self],
            'suppliers': suppliers,
            'suppliers_info': suppliers_info,
        }


class ClientReport(models.AbstractModel):
    _name = 'report.mgmtsystem_process_integration.customer_report'
    _inherit = 'mgmtsystem.code'
    _description = 'Listado de clientes y clientes críticos'

    @api.model
    def _get_report_values(self, docids, data=None):
        critical = False
        if data.get('critical'):
            customers = self.env['res.partner'].search(
                [('customer', '=', 1), ('vip_customer', '=', 1)])
            critical = True
        else:
            customers = self.env['res.partner'].search([('customer', '=', 1)])
        company = self.env.user.company_id

        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': [self],
            'critical': critical,
            'customers': customers,
        }
