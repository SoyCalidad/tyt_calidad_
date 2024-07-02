from odoo import api, fields, models


class CompanypurchaseOnboarding(models.Model):
    _inherit = 'res.company'

    # employee dashboard onboarding
    purchase_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the purchase onboarding panel", default='not_done')
    purchase_product_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the purchase product onboarding panel", default='not_done')
    purchase_order_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the purchase onboarding panel", default='not_done')

    @api.model
    def action_open_purchase_product(self, action_ref=None):
        if not action_ref:
            action_ref = 'soy_calidad_onboarding.action_purchase_product_configurator'
        result = self.env.ref(action_ref).read()[0]
        return result

    @api.model
    def action_open_purchase_order(self, action_ref=None):
        if not action_ref:
            action_ref = 'soy_calidad_onboarding.action_purchase_order_configurator'
        result = self.env.ref(action_ref).read()[0]
        return result

    @api.model
    def action_close_purchase_onboarding(self):
        """ Mark the hr onboarding panel as closed. """
        self.env.company.employee_onboarding_state = 'just_done'

    def get_and_update_purchase_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'purchase_product_onboarding_state',
            'purchase_order_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('purchase_onboarding_state', steps)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_save_onboarding_purchase_product_step(self):
        """ Set the onboarding step as done """
        pass

class PurchaseOrderCalidad(models.Model):
    _inherit = 'purchase.order'

    def action_save_onboarding_purchase_order_step(self):
        """ Set the onboarding step as done """
        pass