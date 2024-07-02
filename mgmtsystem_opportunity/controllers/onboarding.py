from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/opportunity/opportunity_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        opportunity_onboarding_panel = 'mgmtsystem_opportunity.opportunity_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(opportunity_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_opportunity_onboarding_state()
        })
        return {'html': html_content}