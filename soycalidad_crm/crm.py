from odoo import api, fields, models

class CRM(models.Model):
    _inherit = 'crm.lead'

    partner_id = fields.Many2one('res.partner', string='Customer', tracking=10, index=True,
        domain="['|', '|', '|'('company_id', '=', False), ('company_id', '=', company_id), ('user_id','=',user.id), ('user_id','=',False)]", help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")