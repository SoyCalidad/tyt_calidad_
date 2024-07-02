from odoo import api, fields, models


class ApplicantsWizard(models.TransientModel):
    _name = 'applicants.wizard'
    
    closed_included = fields.Boolean(string='Incluir procesos de selección finalizados', )
    

    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'is_wizard': True,
            'ids': self._ids,
            'model': 'applicant.wizard',
            'res_model': 'applicant.wizard',
        }
        return self.env.ref('mgmtsystem_employees.report_applicants_database').report_action(self, data=datas)


class ApplicantsReport(models.AbstractModel):
    _name = 'report.mgmtsystem_employees.applicants_database_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        
        if data and data.get('is_wizard'):
            applicant_ids = self.env['hr.applicant'].search([], order="name asc")
        else:
            applicant_ids = self.env['hr.applicant'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': applicant_ids,
        }
