from odoo import api, fields, models

class CompanyStockOnboarding(models.Model):
    _inherit = 'res.company'

     # employee dashboard onboarding
    stock_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the stock onboarding panel", default='not_done')
    stock_in_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the stock in onboarding panel", default='not_done')
    stock_out_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), (
        'done', "Done"), ('closed', "Closed")], string="State of the stock out onboarding panel", default='not_done')

    @api.model
    def action_open_stock_in(self, action_ref=None):
        if not action_ref:
            action_ref = 'soy_calidad_onboarding.action_stock_in_configurator'
        result = self.env.ref(action_ref).read()[0]
        result['context'] = {'default_picking_type_id': self.env.ref('stock.picking_type_in').id}
        return result

    
    @api.model
    def action_open_stock_out(self, action_ref=None):
        if not action_ref:
            action_ref = 'soy_calidad_onboarding.action_stock_out_configurator'
        result = self.env.ref(action_ref).read()[0]
        result['context'] = {'default_picking_type_id': self.env.ref('stock.picking_type_out').id}
        return result

    @api.model
    def action_close_stock_onboarding(self):
        """ Mark the hr onboarding panel as closed. """
        self.env.company.employee_onboarding_state = 'just_done'

    def get_and_update_stock_onboarding_state(self):
        """ This method is called on the controller rendering method and ensures that the animations
            are displayed only one time. """
        steps = [
            'stock_in_onboarding_state',
            'stock_out_onboarding_state',
        ]
        return self.sudo().get_and_update_onbarding_state('stock_onboarding_state', steps)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_save_onboarding_stock_stock_step(self):
        """ Set the onboarding step as done """
        pass

    def send_validate(self):
        super().send_validate()
        if self.picking_type_code == 'incoming':
            self.env.company.sudo().set_onboarding_step_done(
                'stock_in_onboarding_state')
        if self.picking_type_code == 'outgoing':
            self.env.company.sudo().set_onboarding_step_done(
                'stock_out_onboarding_state')
