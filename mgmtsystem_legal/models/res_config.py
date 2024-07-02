from odoo import fields,models,api, _
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    legal_process_id = fields.Many2one('mgmt.process', domain=[('active','=',True)],string = 'Procedimiento para plan legal',related='company_id.legal_process_id')

class Company(models.Model):
    _inherit = 'res.company'

    legal_process_id = fields.Many2one('mgmt.process', domain=[('active','=',True)],string = 'Procedimiento para plan legal')