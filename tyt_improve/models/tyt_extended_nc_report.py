from odoo import models, api, fields

class ExtendedNcReport(models.TransientModel):
    _inherit = "wizard.nc.report"

    def export_nc_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard.nc.report'
        datas['form'] = self.read()[0]
        datas['code'] = self.code
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('tyt_improve.tyt_report_nc_xlsx').report_action(self, data=datas)

    def export_nc_inventory_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard.nc.report'
        datas['form'] = self.read()[0]
        datas['code'] = self.code
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('tyt_improve.tyt_report_nc_inventory_xlsx').report_action(self, data=datas)
    
    def export_c_evaluation_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard.nc.report'
        datas['form'] = self.read()[0]
        datas['code'] = self.code
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('tyt_improve.tyt_report_c_evaluation_xlsx').report_action(self, data=datas)