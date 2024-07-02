from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/process/process_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        process_onboarding_panel = 'mgmtsystem_process.process_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(process_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_process_onboarding_state()
        })
        return {'html': html_content}


   
