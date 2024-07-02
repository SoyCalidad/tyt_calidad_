from odoo import api, fields, models
from collections import defaultdict


class JobReport(models.AbstractModel):
    _name = 'report.hr_job_functions.reporte_resultados_employees_template'
    _description = 'Manual de organización y funciones'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            job_id = self.env['hr.job'].browse(data['id'])
        else:
            job_id = self.env['hr.job'].browse(docids)
        model_id = self.env['ir.model'].search(
            [('model', '=', 'report.hr_job_functions.reporte_resultados_employees_template')],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code else ''
        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': job_id,
            'code': code,
        }


class EmployeeDataCard(models.AbstractModel):
    _name = 'report.mgmtsystem_employees.report_employees_template'
    _inherit = 'mgmtsystem.code'
    _description = 'Ficha de datos del empleado'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.employee'].browse(docids)
        model_id = self.env['ir.model'].search(
            [('model', '=', 'report.mgmtsystem_employees.report_employees_template')],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code else ''
        return {
            'docs': docs,
            'doc_ids': self.ids,
            'code': code,
        }
