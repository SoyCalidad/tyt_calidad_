from odoo import http
from odoo.http import request


class OnboardingController(http.Controller):

    @http.route('/onboarding/stock_onboarding', auth='user', type='json')
    def stock_onboarding(self):

        company = request.env.company
        stock_onboarding_panel = 'soy_calidad_onboarding.stock_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(stock_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_stock_onboarding_state()
        })
        return {'html': html_content}





    @http.route('/onboarding/purchase_onboarding', auth='user', type='json')
    def purchase_onboarding(self):
        company = request.env.company
        purchase_onboarding_panel = 'soy_calidad_onboarding.purchase_onboarding_panel'
        qweb = request.env['ir.qweb']
        html_content = qweb._render(purchase_onboarding_panel, {
            'company': company,
            'state': company.get_and_update_purchase_onboarding_state()
        })
        return {'html': html_content}



        return {
            'html': request.env.ref('soy_calidad_onboarding.purchase_onboarding_panel').render({
                'company': company,
                'state': company.get_and_update_purchase_onboarding_state()
            })
        }
