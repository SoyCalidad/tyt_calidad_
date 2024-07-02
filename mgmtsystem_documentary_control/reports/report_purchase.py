from odoo import api, models


class PurchaseReport(models.AbstractModel):
    _name = 'report.purchase.report_purchaseorder'
    _description = 'Orden de compra (Reporte)'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['purchase.order'].browse(docids)
        model_id = self.env['ir.model'].search(
            [('model', '=', 'report.purchase.report_purchaseorder')],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code else ''
        print ('Código: ', code)
        return {
            'docs': docs,
            'code': code,
        }


class PurchaseReport(models.AbstractModel):
    _name = 'report.purchase.report_purchasequotation'
    _description = 'Solicitud de presupuesto (Reporte)'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['purchase.order'].browse(docids)
        model_id = self.env['ir.model'].search(
            [('model', '=', 'report.purchase.report_purchasequotation')],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code else ''
        return {
            'docs': docs,
            'code': code,
        }
