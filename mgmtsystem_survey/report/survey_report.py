from odoo import api, fields, models
from odoo.exceptions import UserError


class SurveyReportWizard(models.TransientModel):
    _name = 'survey_report.wizard'

    survey_id = fields.Many2one(
        'survey.survey', string='Encuesta', required=True)

    def action_print(self):
        report_id = ''
        type_action = self._context.get('type_action', '')
        if type_action == '':
            return
        elif type_action == 'report':
            report_id = 'mgmtsystem_survey.reporte_survey'
        elif type_action == 'analysis':
            report_id = 'mgmtsystem_survey.action_report_survey_report'

        if not report_id:
            return
        res = self.env.ref(report_id).report_action(self.survey_id)
        return res


class SurveyReport1(models.AbstractModel):
    _name = 'report.mgmtsystem_survey.reporte_encuestas_template'
    _description = 'Informe de encuesta'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['survey.survey'].browse(docids)
        model_id = self.env['ir.model'].search(
            [('model', '=', 'report.mgmtsystem_survey.reporte_encuestas_template')],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code and code.code else ''
        return {
            'docs': docs,
            'code': code,
        }
