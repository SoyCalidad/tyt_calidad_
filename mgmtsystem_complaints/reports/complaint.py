from odoo import api, fields, models


class ComplaintReport(models.AbstractModel):
    _name = 'report.mgmtsystem_complaints.complaint_report_list'
    _description = 'Lista de quejas y reclamos'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['complaint.complaint'].browse(docids)
        model_id = self.env['ir.model'].search(
            [('model', '=', self._name)],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code and code.code else ''
        return {
            'docs': docs,
            'code': code,
        }
