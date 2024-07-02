from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/complaints/complaints_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        complaints_onboarding_panel = 'mgmtsystem_complaints.complaints_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(complaints_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_complaints_onboarding_state()
        })
        return {'html': html_content}