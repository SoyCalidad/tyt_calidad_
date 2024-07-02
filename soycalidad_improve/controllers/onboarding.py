from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/improve/improve_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        improve_onboarding_panel = 'soycalidad_improve.improve_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(improve_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_improve_onboarding_state()
        })
        return {'html': html_content}




