from odoo import api, models
from odoo.tools import is_html_empty


class IrModelReferenceReport(models.AbstractModel):
    _inherit = 'report.base.report_irmodulereference'


    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('base.report_irmodulereference')
        selected_modules = self.env['ir.module.module'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'model_description': report.model_id.name,
            'docs': selected_modules,
            'findobj': self._object_find,
            'findfields': self._fields_find,
        }


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def _get_rendering_context(self, report, docids, data):
        # If the report is using a custom model to render its html, we must use it.
        # Otherwise, fallback on the generic html rendering.
        report_model = self._get_rendering_context_model(report)

        data = data and dict(data) or {}

        if report_model is not None:
            data['model_description'] = self.name
            data.update(report_model._get_report_values(docids, data=data))
        else:
            docs = self.env[self.model].browse(docids)
            data.update({
                'doc_ids': docids,
                'doc_model': self.model,
                'model_description': self.name,
                'docs': docs,
            })
            
        data['is_html_empty'] = is_html_empty

        return data