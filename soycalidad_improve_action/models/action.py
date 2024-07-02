from odoo import api, fields, models


class MgmtsystemAction(models.Model):
    _name = 'mgmtsystem.action'
    _inherit = ['mgmtsystem.action']

    recurring = fields.Boolean('Recurring')

    @api.onchange('date_deadline', 'recurring')
    def on_date_deadline_change(self):
        if self.recurring:
            self.date_deadline = False
