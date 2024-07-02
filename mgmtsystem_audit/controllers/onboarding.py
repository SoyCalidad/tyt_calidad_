from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/audit/audit_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        audit_onboarding_panel = 'mgmtsystem_audit.audit_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(audit_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_audit_onboarding_state()
        })
        return {'html': html_content}


