from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/mgmt_review/mgmt_review_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        mgmt_review_onboarding_panel = 'mgmtsystem_management_review.mgmt_review_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(mgmt_review_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_mgmt_review_onboarding_state()
        })
        return {'html': html_content}
