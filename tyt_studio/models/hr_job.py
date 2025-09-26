from odoo import models, fields 


class HrJob(models.Model):
    _inherit = "hr.job"
    
    nesp = fields.Char(string="nesp")
