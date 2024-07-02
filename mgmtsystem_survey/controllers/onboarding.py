from odoo import http
from odoo.http import request

class OnboardingController(http.Controller):
    @http.route('/survey/survey_onboarding', auth='user', type='json')
    def account_invoice_onboarding(self):
        company = request.env.company
        survey_onboarding_panel = 'mgmtsystem_survey.survey_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(survey_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_survey_onboarding_state()
        })
        return {'html': html_content}