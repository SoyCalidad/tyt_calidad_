from odoo import api, models, fields
from random import randint


class ResPartnerCustomerCampaign(models.Model):
    _name = 'res.partner.customer_campaign'
    _description = 'Customer Campaign'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color', default=_get_default_color)
    active = fields.Boolean(string='Active', default=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_campaign_ids = fields.Many2many('res.partner.customer_campaign', string='Customer Campaigns')
    observations = fields.Text(string='Observations')

    property_date = fields.Date(string='Property Date')
    property_client = fields.Char(string='Property Client', compute='_compute_property_client', readonly=False, store=True)
    property_name = fields.Text(string='Property Name')
    property_activity = fields.Text(string='Property Activity')
    property_inadequate_condition = fields.Text(string='Property Inadequate Condition')
    property_response_activity_ids = fields.Many2many('mgmtsystem.action', string='Property Actions')
    property_corrective_action_initiated = fields.Boolean(string='Property Corrective Action Initiated', default=False)
    evaluation_qualification = fields.Selection([
        ('a', 'A - Excepcional'),
        ('b', 'B - Aceptable'),
        ('c', 'C - Aceptable con prueba adicional'),
        ('d', 'D - Inaceptable'),
    ], string='Evaluation Qualification')

    @api.depends('customer', 'name')
    def _compute_property_client(self):
        for record in self:
            if record.customer:
                record.property_client = record.name
            else:
                record.property_client = False
