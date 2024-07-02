from odoo import api, fields, models

class CrmUserTransfer(models.TransientModel):
    _name = 'crm.user_transfer'
    _description = 'Crm User Transfer'
    
    lead_ids = fields.Many2many('crm.lead', string='Oportunidades')
    user_id = fields.Many2one('res.users', string='Vendedor')

    def transfer_user(self):
        if self.user_id:
            for lead in self.lead_ids:
                lead.user_id = self.user_id.id

    def transfer_all(self):
        lead_ids = self.env['crm.lead'].search([])
        if self.user_id:
            for lead in lead_ids:
                lead.user_id = self.user_id.id