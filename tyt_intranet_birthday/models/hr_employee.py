from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import date


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_birthday = fields.Boolean(string='Is Birthday', compute='_compute_is_birthday', store=True)
    is_birthday_this_week = fields.Boolean(string='Is Birthday This Week', compute='_compute_is_birthday', store=True)
    is_birthday_this_month = fields.Boolean(string='Is Birthday This Month', compute='_compute_is_birthday', store=True)
    include_in_birthday_publication = fields.Boolean(string='Include in Birthday Publication', default=True)
    include_in_all_birthday_publications = fields.Boolean(string='Include in All Birthday Publications', default=False)
    birthday_card = fields.Binary(string='Birthday Card')
    birthday_card_filename = fields.Char(string='Birthday Card Filename')
    has_uploaded_custom_card = fields.Boolean(string='Has Uploaded Custom Card')
    birthday_publication_ids = fields.Many2many('tyt.intranet.birthday_publication', 'birthday_publication_employee_rel',
                                                'employee_id', 'publication_id', string='Birthday Publications')

    @api.depends('birthday')
    def _compute_is_birthday(self):
        today = date.today()
        start_of_week = today - relativedelta(days=today.weekday())
        end_of_week = start_of_week + relativedelta(days=6)
        for employee in self:
            if employee.birthday:
                current_year_birthday = employee.birthday.replace(year=today.year)
                employee.is_birthday = current_year_birthday == today
                employee.is_birthday_this_week = start_of_week <= current_year_birthday <= end_of_week
                employee.is_birthday_this_month = employee.birthday.month == today.month
            else:
                employee.is_birthday = False
                employee.is_birthday_this_week = False
                employee.is_birthday_this_month = False

    @api.model
    def _cron_update_birthday_status(self):
        employees = self.env['hr.employee'].search([('birthday', '!=', False)])
        employees._compute_is_birthday()
        group_map = {}
        for emp in employees:
            combo_key = (
                emp.is_birthday,
                emp.is_birthday_this_week,
                emp.is_birthday_this_month
            )
            group_map.setdefault(combo_key, self.env['hr.employee'])
            group_map[combo_key] += emp

        for combo_key, emp_group in group_map.items():
            emp_group.write({
                'is_birthday': combo_key[0],
                'is_birthday_this_week': combo_key[1],
                'is_birthday_this_month': combo_key[2],
            })
