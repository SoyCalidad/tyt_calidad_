from collections import defaultdict

from odoo import api, fields, models


class ComplaintReport(models.AbstractModel):
    _name = 'report.mgmtsystem_process.reporte_process_hola_calidad_template'
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

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': new_process,
            'color': color,
            'code': '-',
        }
