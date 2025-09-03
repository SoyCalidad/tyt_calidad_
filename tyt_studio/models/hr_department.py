from odoo import models, fields, api 


class HrDeparment(models.Model):
    _inherit = "hr.department"
    
    sitio = fields.Many2one('tyt_studio.site', ondelete="set null")