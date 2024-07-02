from odoo import api, fields, models

class CertificateWizard(models.TransientModel):
    _name = 'training.certificate.wizard'
    _description = 'Wizard de Certificado de capacitación'

    training_ids = fields.Many2many('mgmtsystem.plan.training', string='Capacitaciones')
    employee_ids = fields.Many2many('hr.employee', string='Empleados')

    def action_print_certificate_trainings(self):
        cert_ids = []
        for tra in self.training_ids:
            for line in tra.line_ids:
                if line.employee_id and line.assistance == 'A':
                    cert_ids.append(line.id)
        datas = {
            'cert_ids': cert_ids,
        }
        return self.env.ref('mgmtsystem_employees.action_report_training_certificate').report_action(self, data=datas)

    def action_print_certificate_employees(self):
        cert_ids = []
        # tra = self.env['mgmtsystem.plan.training.line'].search([('employee_id', 'in', self.employee_ids), ('', '=', )])
        for emp in self.employee_ids:
            for line in emp.training_line_ids:
                if line.assistance == 'A':
                    cert_ids.append(line.id)
        datas = {
            'cert_ids': cert_ids,
        }
        return self.env.ref('mgmtsystem_employees.action_report_training_certificate').report_action(self, data=datas)

class TrainingCertificateReport(models.AbstractModel):
    _name = 'report.mgmtsystem_employees.report_training_certificate'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('cert_ids'):
            training_line_ids = self.env['mgmtsystem.plan.training.line'].browse(data['cert_ids'])
        else:
            training_line_ids = self.env['mgmtsystem.plan.training.line'].browse(docids)
        company = self.env.user.company_id

        return {
            'doc_ids': self.ids,
            'docs': training_line_ids,
            'company': company,
        }