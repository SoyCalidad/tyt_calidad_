from odoo import fields,models,api, _
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    training_process_id = fields.Many2one('mgmt.process',string = 'Procedimiento para capacitaciones',related='company_id.training_process_id', domain=[('active','=',True)])

class Company(models.Model):
    _inherit = 'res.company'

    training_process_id = fields.Many2one('mgmt.process', string = 'Procedimiento para capacitaciones', domain=[('active','=',True)])