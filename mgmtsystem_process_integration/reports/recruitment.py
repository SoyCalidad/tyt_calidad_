from odoo import api, fields, models
from collections import defaultdict


class RecruitmentReport(models.AbstractModel):
    _name = 'report.mgmtsystem_employees.report_applicant'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            applicant_id = self.env['hr.applicant'].browse(data['id'])
        else:
            applicant_id = self.env['hr.applicant'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': applicant_id,
        }


class RecruitmentReportWizard(models.TransientModel):
    _name = 'hr.applicant.report.wizard'

    applicant_id = fields.Many2one(
        'hr.applicant', string='Solicitudes', required=True)

    def action_print(self):
        id = self.applicant_id.id
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'model': 'hr.applicant.report.wizard',
            'res_model': 'hr.applicant.report.wizard',
            'is_wizard': True,
            'id': id,
        }
        return self.env.ref('mgmtsystem_employees.action_report_applicant').report_action(self, data=datas)


class GeneralRecruitmentReport(models.AbstractModel):
    _name = 'report.mgmtsystem_employees.report_general_applicant'

    @api.model
    def _get_report_values(self, docids, data=None):
        applicant_ids = self.env['hr.applicant'].browse(data['id'])

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': applicant_ids,
        }


class GeneralRecruitmentReportWizard(models.TransientModel):
    _name = 'hr.general.applicant.report.wizard'

    applicant_ids = fields.Many2many('hr.applicant', string='Solicitudes')

    def action_print(self):
        ids = self.applicant_ids.ids
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'model': 'hr.general.applicant.report.wizard',
            'res_model': 'hr.general.applicant.report.wizard',
            'is_wizard': True,
            'id': ids,
        }
        return self.env.ref('mgmtsystem_employees.action_report_applicant').report_action(self, data=datas)

class PorterForcesReportXLS(models.AbstractModel):
    _name = 'report.mgmtsystem_process_integration.general_applicant_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        """Generate a xls report with the data

        Arguments:
            workbook {object} -- A object that represents a Excel workbook
            data {dict} -- The data of the report
            partners {object} -- A class object

        Raises:
            UserError: When the user choose a initial balance but no a initial date
        """
        
        partners = self.env['hr.applicant'].browse(data['id'])
        
        format_title = workbook.add_format(
            {'font_size': 13, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'align': 'center', 'border': True, 'bg_color': '#EEEEEE'})
        format_data = workbook.add_format(
            {'font_size': 9, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'border': True})
        format_header = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'border': True, 'text_wrap': True, 'bold': True, 'align': 'center', 'bg_color': '#EEEEEE'})
        format_text = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'border': True, 'align': 'center', 'text_wrap': True, 'valign': 'vcenter'})

        sheet = workbook.add_worksheet('Indicadores')
        sheet.set_column('A:H', 18)
        sheet.set_column('F:H', 30)
