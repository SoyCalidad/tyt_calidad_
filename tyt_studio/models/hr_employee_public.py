from odoo import fields, models 

class HrEmployeePulic(models.Model):
    _inherit = "hr.employee.public"
    
    sitio = fields.Many2one('tyt_studio.site', ondelete="set null", string="Sitio")
    numero = fields.Char(string="Numero")
    sitios0 = fields.Many2one('tyt_studio.sites', ondelete="set null", string="Sitios0")
    
