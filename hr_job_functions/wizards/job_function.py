from odoo import api, models, fields


class JobFunctionWizard(models.TransientModel):
    _name = 'mgmt.job_function.report.wizard'

    job_id = fields.Many2one('hr.job', string='Puesto', required=True)

    def action_print(self):
        id = self.job_id.id
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'model': 'mgmt.job_function.report.wizard',
            'res_model': 'mgmt.job_function.report.wizard',
            'id': id,
            'is_wizard': True,
        }
        return self.env.ref('hr_job_functions.report_funinings').report_action(self, data=datas)


class EmployeeReportWizard(models.TransientModel):
    _name = 'mgmt.employee.report.wizard'
    _inherit = 'mgmtsystem.code'
    _description = 'Wizard de Ficha de empleado'

    employee_id = fields.Many2one(
        'hr.employee', string='Empleado', required=True)

    def action_print(self):
        employee_id = self.employee_id
        report = self.env.ref('mgmtsystem_employees.action_report_hr_employee_data').report_action(
            employee_id)
        return report
