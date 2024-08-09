from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    job_id = fields.Many2one(related='employee_id.job_id', readonly=False, related_sudo=False)
