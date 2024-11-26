from odoo import api, fields, models, _
from odoo.exceptions import UserError
from random import randint
from datetime import date
import random


class ResUsers(models.Model):
    _inherit = 'res.users'

    show_birthday_card_modal = fields.Boolean(string="Show Birthday Card Modal",
                                              compute='_compute_show_birthday_card_modal', store=False)

    @api.depends('partner_id')
    def _compute_show_birthday_card_modal(self):
        for user in self:
            # Get the employee linked to the user
            employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
            if not employee:
                user.show_birthday_modal = False
                continue

            # Check if the employee is in the birthday list
            birthday_today = self.env['tyt.intranet.birthday_publication'].search([
                ('today', '=', fields.Date.today()),
                ('birthday_daily_ids.employee_id', '=', employee.id),
            ])
            user.show_birthday_modal = bool(birthday_today)
