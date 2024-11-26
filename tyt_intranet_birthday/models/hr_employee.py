from odoo import api, fields, models, _
from odoo.exceptions import UserError
from random import randint
from datetime import date
import random


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_birthday = fields.Boolean(string='Is Birthday', compute='_compute_is_birthday', store=False)
    include_in_birthday_publication = fields.Boolean(string='Include in Birthday Publication', default=True)
    include_in_all_birthday_publications = fields.Boolean(string='Include in All Birthday Publications', default=False)
    birthday_card = fields.Binary(string='Birthday Card')
    birthday_card_filename = fields.Char(string='Birthday Card Filename')

    def _compute_is_birthday(self):
        for employee in self:
            today = fields.Date.today()
            if employee.birthday and employee.birthday.day == today.day and employee.birthday.month == today.month:
                employee.is_birthday = True
            else:
                employee.is_birthday = False
