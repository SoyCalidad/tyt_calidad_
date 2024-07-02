from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/context/context_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        context_onboarding_panel = 'mgmtsystem_context.context_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(context_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_context_onboarding_state()
        })
        return {'html': html_content}
