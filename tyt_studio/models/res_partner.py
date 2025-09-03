from odoo import models, fields 


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    empleado = fields.Many2one('hr.employee', ondelete="set null", string="Empleado")
    usuario = fields.Many2one('res.users', string="Usuario", ondelete="set null")