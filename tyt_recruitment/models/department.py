from odoo import api, models, fields

class DeparmentDays(models.Model):
    _inherit = 'hr.department'

    days = fields.Integer( string="Días de capacitación")