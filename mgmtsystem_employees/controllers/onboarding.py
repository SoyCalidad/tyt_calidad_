from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/training/training_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        training_onboarding_panel = 'mgmtsystem_employees.training_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(training_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_training_onboarding_state()
        })
        return {'html': html_content}
        

    @http.route('/employee/employee_onboarding', auth='user', type='json')
    def hr_employee_onboarding(self):
        company = request.env.company
        employee_onboarding_panel = 'mgmtsystem_employees.employee_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(employee_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_employee_onboarding_state()
        })
        return {'html': html_content}
