from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    intranet_user_ids = fields.One2many('res.users', 'x_studio_empleado', string='Intranet Users')
    intranet_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Intranet User',
        compute='_compute_intranet_user_id',
        search='_search_intranet_user_id',
        store=False,
    )

    @api.depends('intranet_user_ids')
    def _compute_intranet_user_id(self):
        user_per_employee = {
            user.x_studio_empleado: user
            for user in self.env['res.users'].search([('x_studio_empleado', 'in', self.ids)])
        }
        for employee in self:
            employee.intranet_user_id = user_per_employee.get(employee)

    def _search_intranet_user_id(self, operator, value):
        return [('intranet_user_ids', operator, value)]
