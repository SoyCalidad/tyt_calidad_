from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/legal/legal_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        legal_onboarding_panel = 'mgmtsystem_legal.legal_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(legal_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_legal_onboarding_state()
        })
        return {'html': html_content}