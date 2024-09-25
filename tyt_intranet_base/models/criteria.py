from odoo import api, fields, models, _


class Criteria(models.Model):
    _name = 'intranet.criteria'
    _description = 'Criteria'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    department_id = fields.Many2one('hr.department', string='Department')
    job_id = fields.Many2one('hr.job', string='Job Position')
    employee_ids = fields.Many2many('hr.employee', string='Employees')
    employee_count = fields.Integer(compute='_compute_employee_count', string='Employee Count')
    excluded_employee_ids = fields.Many2many(
        comodel_name='hr.employee',
        relation='intranet_criteria_hr_employee_rel',
        column1='criteria_id',
        column2='employee_id',
        string='Excluded Employees'
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.user.company_id.id,
        domain=lambda self: [('id', 'in', self.env.user.company_ids.ids)],
    )
    user_ids = fields.Many2many('res.users', string='Users')
    user_count = fields.Integer(compute='_compute_user_count', string='User Count')

    @api.depends('employee_ids')
    def _compute_employee_count(self):
        for record in self:
            record.employee_count = len(record.employee_ids)

    @api.depends('user_ids')
    def _compute_user_count(self):
        for record in self:
            record.user_count = len(record.user_ids)

    def action_filter_employees_by_criteria(self):
        domain = []
        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))
        if self.job_id:
            domain.append(('job_id', '=', self.job_id.id))
        if domain:
            employees = self.env['hr.employee'].search(domain)
        else:
            employees = self.env['hr.employee'].search([])
        employees = employees - self.excluded_employee_ids
        users = employees.mapped('user_id')
        self.employee_ids = [(6, 0, employees.ids)]
        self.user_ids = [(6, 0, users.ids)]

    def action_show_employees(self):
        self.ensure_one()
        return {
            'name': _('Employees'),
            'view_mode': 'tree,form',
            'res_model': 'hr.employee',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('id', 'in', self.employee_ids.ids)],
            'target': 'current',
        }

    def action_show_users(self):
        self.ensure_one()
        return {
            'name': _('Users'),
            'view_mode': 'tree,form',
            'res_model': 'res.users',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('id', 'in', self.user_ids.ids)],
            'target': 'current',
        }
