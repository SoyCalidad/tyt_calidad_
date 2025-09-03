from odoo import fields, models 

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    
    sitio = fields.Many2one('tyt_studio.site', ondelete="set null", string="Sitio")
    numero = fields.Char(string="Numero")
    sitios0 = fields.Many2one('tyt_studio.sites', ondelete="set null", string="Sitios0")
    
    segurosocial = fields.Char(string="Seguro social", )