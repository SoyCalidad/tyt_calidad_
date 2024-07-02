from odoo import fields,models,api, _
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    infrastructure_process_id = fields.Many2one('mgmt.process', domain=[('active','=',True)],string = 'Procedimiento para infraestructura',related='company_id.infrastructure_process_id')
    maintenance_process_id = fields.Many2one('mgmt.process', domain=[('active','=',True)],string = 'Procedimiento para mantenimientos',related='company_id.maintenance_process_id')

class Company(models.Model):
    _inherit = 'res.company'

    infrastructure_process_id = fields.Many2one('mgmt.process', domain=[('active','=',True)],string = 'Procedimiento para infraestructura')
    maintenance_process_id = fields.Many2one('mgmt.process', domain=[('active','=',True)],string = 'Procedimiento para mantenimientos')