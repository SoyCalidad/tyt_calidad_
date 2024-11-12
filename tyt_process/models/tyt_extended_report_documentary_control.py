from odoo import models, api, fields

class ExtendedNcReport(models.TransientModel):
    _name = 'wizard.inventory.report'
    _description = 'Wizard para Reporte de Inventario'

    date_init = fields.Date(string='Fecha de Inicio')
    date_fin = fields.Date(string='Fecha de Fin')

    def export_external_inventory_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard.inventory.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('tyt_process.action_external_inventory_report').report_action(self, data=datas)

    def export_internal_inventory_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard.inventory.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('tyt_process.action_internal_inventory_report').report_action(self, data=datas)