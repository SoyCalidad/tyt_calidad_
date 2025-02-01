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
    birthday_publication_ids = fields.Many2many(
        'tyt.intranet.birthday_publication', 
        'birthday_publication_employee_rel', 'employee_id', 'publication_id', 
        string='Birthday Publications',
    )
    birthday_month = fields.Integer(string="Birthday Month", compute='_compute_birthday_month', store=True)

    @api.depends('birthday')
    def _compute_birthday_month(self):
        for rec in self:
            rec.birthday_month = rec.birthday and rec.birthday.month or False

    @api.depends('birthday')
    def _compute_is_birthday(self):
        today = date.today()
        for employee in self:
            flags = self._get_birthday_flags(employee, today)
            employee.is_birthday = flags['is_birthday']
            employee.is_birthday_this_week = flags['is_birthday_this_week']
            employee.is_birthday_this_month = flags['is_birthday_this_month']

    def _get_birthday_flags(self, employee, today):
        start_of_week = today - relativedelta(days=today.weekday())
        end_of_week = start_of_week + relativedelta(days=6)
        if employee.birthday:
            try:
                current_year_birthday = employee.birthday.replace(year=today.year)
            except ValueError:
                current_year_birthday = employee.birthday + relativedelta(years=today.year - employee.birthday.year)
            return {
                'is_birthday': current_year_birthday == today,
                'is_birthday_this_week': start_of_week <= current_year_birthday <= end_of_week,
                'is_birthday_this_month': employee.birthday.month == today.month,
            }
        return {
            'is_birthday': False,
            'is_birthday_this_week': False,
            'is_birthday_this_month': False,
        }

    @api.model
    def update_birthday_status(self):
        today = date.today()
        start_of_week = today - relativedelta(days=today.weekday())
        end_of_week = start_of_week + relativedelta(days=6)
        relevant_months = {start_of_week.month, today.month, end_of_week.month}

        employees = self.search([
            ('birthday', '!=', False),
            '|',
            ('is_birthday_this_month', '=', True),
            ('birthday_month', 'in', list(relevant_months)),
        ])

        group_map = {}
        for emp in employees:
            flags = self._get_birthday_flags(emp, today)
            combo_key = (flags['is_birthday'], flags['is_birthday_this_week'], flags['is_birthday_this_month'])
            group_map.setdefault(combo_key, self.env['hr.employee'])
            group_map[combo_key] |= emp

        for combo_key, emp_group in group_map.items():
            emp_group.write({
                'is_birthday': combo_key[0],
                'is_birthday_this_week': combo_key[1],
                'is_birthday_this_month': combo_key[2],
            })
