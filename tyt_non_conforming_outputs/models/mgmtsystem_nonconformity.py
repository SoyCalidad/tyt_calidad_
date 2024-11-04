from odoo import models, fields

class MgmtSystemNonconformity(models.Model):
    _inherit = 'mgmtsystem.nonconformity'

    client_id = fields.Many2one('res.partner', string='Client')
    penalty_ids = fields.Many2many('penalty.tag', string="Penalty")
    penalty_negotiation_clients = fields.Text(string='Penalty Negotiation with Clients')


class PenaltyTag(models.Model):
    _name = 'penalty.tag'
    _description = 'Penalty Tag'

    name = fields.Char(string='Penalty Name', required=True)