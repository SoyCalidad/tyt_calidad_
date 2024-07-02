from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/comunication/comunication_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        comunication_onboarding_panel = 'mgmtsystem_comunication.comunication_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(comunication_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_comunication_onboarding_state()
        })
        return {'html': html_content}
