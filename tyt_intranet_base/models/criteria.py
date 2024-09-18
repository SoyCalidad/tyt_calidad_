from odoo import fields, models


class Criteria(models.Model):
    _name = 'intranet.criteria'
    _description = 'Criteria'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre')
    department_id = fields.Many2one('hr.department', string='Departmento')
    job_id = fields.Many2one('hr.job', string='Puesto de trabajo')
    sites_id = fields.Many2one('x_sitios', string='Sitios0')
    employee_ids = fields.Many2many('hr.employee', string='Empleados')
    excluded_employee_ids = fields.Many2many(
        comodel_name='hr.employee',
        relation='intranet_criteria_hr_employee_rel',
        column1='criteria_id',
        column2='employee_id',
        string='Empleados excluidos'
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Compañía',
        default=lambda self: self.env.user.company_id.id,
        domain=lambda self: [('id', 'in', self.env.user.company_ids.ids)],
    )

    def action_filter_employees_by_criteria(self):
        domain = []
        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))
        if self.job_id:
            domain.append(('job_id', '=', self.job_id.id))
        if self.sites_id:
            domain.append(('x_studio_sitios0', '=', self.sites_id.id))
        if domain:
            employees = self.env['hr.employee'].search(domain)
        else:
            employees = self.env['hr.employee'].search([])
        employees = employees - self.excluded_employee_ids
        self.employee_ids = [(6, 0, employees.ids)]
