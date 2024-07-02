from odoo import api, fields, models
from collections import defaultdict


class TargetSourceReport(models.TransientModel):
    _name = 'target.source.report'
    _inherit = 'mgmtsystem.code'
    _description = 'Wizard de listado de objetivos e indicadores'

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')

    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'code': self.code,
            'docs': self.target_ids,
        }
        return self.env.ref('mgmtsystem_target.action_report_target_source1').report_action(self.target_ids)

class ReportMgmtsystemTargetTargetSourceReport(models.AbstractModel):
    _name = 'report.mgmtsystem_target.target_source_report'
    _description = 'Listado de objetivos e indicadores'

    @api.model
    def _get_report_values(self, docids, data=None):
        model_id = self.env['ir.model'].search(
            [('model', '=', self._name)],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code else ''
        docs = self.env['mgmtsystem.target'].browse(docids)
        return {
            'doc_ids': self.ids,
            'code': code,
            'docs': docs,
        }

    
    