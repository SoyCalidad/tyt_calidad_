from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/general/general_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        if not request.env.is_admin() or company.general_onboarding_state == 'closed':
            return {}

        general_onboarding_panel = 'menus_hola_calidad.general_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(general_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_general_onboarding_state()
        })
        return {'html': html_content}

