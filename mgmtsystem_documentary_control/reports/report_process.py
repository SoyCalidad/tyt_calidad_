from collections import defaultdict

from odoo import api, models


class ComplaintReport(models.AbstractModel):
    _name = 'report.mgmtsystem_process.reporte_process_hola_calidad_template'
    _inherit = [
        'report.mgmtsystem_process.reporte_process_hola_calidad_template', 'mgmtsystem.code']
    _description = 'Mapa de procesos'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data.get('is_wizard'):
            if data['ids_']:
                process = self.env['mgmt.categ'].browse(
                    data['ids_'],)
            elif not data['ids_']:
                process = self.env['mgmt.categ'].search([],)
        else:
            process = self.env['mgmt.categ'].browse(docids,)

        groups = defaultdict(list)
        color = {}

        for obj in process:
            color[obj.color] = str(obj.comments)
            groups[obj.type].append(obj)

        new_process = groups.values()

        new_process = list(new_process)

        end_list = {}
        
        model_id = self.env['ir.model'].search([('model', '=', 'report.mgmtsystem_process.reporte_process_hola_calidad_template')], limit=1)
        code = self.env['documentary.control'].search([('model_id','=',model_id.id)], limit=1)

        company = self.env.user.company_id
        code = code.code if code else ''
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': new_process,
            'color': color,
            'code': code,
        }
