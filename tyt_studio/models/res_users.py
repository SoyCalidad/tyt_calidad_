from odoo import fields, models, api 

class ResUsers(models.Model):
    _inherit = "res.users"
    
    empleado = fields.Many2one('hr.employee', ondelete="set null")
    numero = fields.Char(string="Número de empleado", readonly=True)
    sitio = fields.Many2one('tyt_studio.site', ondelete="set null", string="Sitio0")
    