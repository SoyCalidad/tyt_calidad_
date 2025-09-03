from odoo import models, fields 

class ResGroups(models.Model):
    _inherit = "res.groups"
    
    job_id = fields.Many2one('hr.job', ondelete="set null", string="Job")