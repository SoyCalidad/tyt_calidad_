from odoo import fields,models,api, _
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    training_process_id = fields.Many2one('mgmt.process', domain=[('active','=',True)],string = 'Procedimiento para capacitaciones',related='company_id.training_process_id')

class Company(models.Model):
    _inherit = 'res.company'

    training_process_id = fields.Many2one('mgmt.process', domain=[('active','=',True)],string = 'Procedimiento para capacitaciones')