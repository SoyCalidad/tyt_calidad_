from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/target/target_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        target_onboarding_panel = 'mgmtsystem_target.target_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(target_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_target_onboarding_state()
        })
        return {'html': html_content}
