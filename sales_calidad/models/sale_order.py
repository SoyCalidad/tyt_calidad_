from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_unique_shipping_address = fields.Boolean(string='Do you have a unique delivery address?', default=False)
    unique_shipping_address = fields.Char(string='Unique delivery address', required=False)
    
    @api.onchange('partner_id')
    def _onchange_partner_id_set_pricelist(self):
        if self.partner_id and self.partner_id.grupo:  # Asumiendo que el campo se llama "grupo" y es de tipo Char
            # Buscar la lista de precios que tiene el mismo nombre que el grupo del cliente
            pricelist = self.env['product.pricelist'].search([('name', '=', self.partner_id.grupo)], limit=1)
            if pricelist:
                self.pricelist_id = pricelist.id
            else:
                # Opción si no se encuentra una lista de precios con el mismo nombre
                self.pricelist_id = False
        else:
            # En caso de que el cliente no tenga grupo o no se encuentre una lista de precios
            self.pricelist_id = False
