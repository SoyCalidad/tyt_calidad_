from odoo import api, fields, models, _


class Groups(models.Model):
    _name = 'intranet.groups'
    _description = 'Intranet Access Groups'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    department_id = fields.Many2one('hr.department', string='Department')
    sitio_id = fields.Many2one(related='department_id.x_studio_sitio', string='Site', store=True)
    job_id = fields.Many2one('hr.job', string='Job Position')
    employee_ids = fields.Many2many(
        comodel_name='hr.employee',
        relation='intranet_groups_employees_rel',
        column1='gid',
        column2='uid',
        String='Employees',
    )
    employee_count = fields.Integer(compute='_compute_employee_count', string='Employee Count')
    user_ids = fields.Many2many('res.users', string='Users')
    user_count = fields.Integer(compute='_compute_user_count', string='User Count')
    implied_ids = fields.Many2many('intranet.groups', 'intranet_groups_implied_rel', 'gid', 'hid',
        string='Inherits', help='Employees of this group automatically inherit those groups')
    trans_implied_ids = fields.Many2many('intranet.groups', string='Transitively inherits',
        compute='_compute_trans_implied', recursive=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.user.company_id.id,
        domain=lambda self: [('id', 'in', self.env.user.company_ids.ids)],
    )

    @api.depends('implied_ids.trans_implied_ids')
    def _compute_trans_implied(self):
        for g in self:
            g.trans_implied_ids = g.implied_ids | g.implied_ids.trans_implied_ids

    @api.model_create_multi
    def create(self, vals_list):
        employee_ids_list = [vals.pop('employee_ids', None) for vals in vals_list]
        groups = super().create(vals_list)
        for group, employee_ids in zip(groups, employee_ids_list):
            if employee_ids:
                group.write({'employee_ids': employee_ids})
        return groups

    def write(self, values):
        res = super().write(values)
        if values.get('employee_ids') or values.get('implied_ids'):
            for group in self:
                self._cr.execute("""
                        WITH RECURSIVE group_imply(gid, hid) AS (
                            SELECT gid, hid
                              FROM intranet_groups_implied_rel
                             UNION
                            SELECT i.gid, r.hid
                              FROM intranet_groups_implied_rel r
                              JOIN group_imply i ON (i.hid = r.gid)
                        )
                        INSERT INTO intranet_groups_employees_rel (gid, uid)
                             SELECT i.hid, r.uid
                               FROM group_imply i, intranet_groups_employees_rel r
                              WHERE r.gid = i.gid
                                AND i.gid = %(gid)s
                             EXCEPT
                             SELECT r.gid, r.uid
                               FROM intranet_groups_employees_rel r
                               JOIN group_imply i ON (r.gid = i.hid)
                              WHERE i.gid = %(gid)s
                    """, dict(gid=group.id))
        return res

    @api.depends('employee_ids')
    def _compute_employee_count(self):
        for record in self:
            record.employee_count = len(record.employee_ids)
            record.user_ids = [(6, 0, record.employee_ids.mapped('x_studio_ususrio').ids)]

    @api.depends('user_ids')
    def _compute_user_count(self):
        for record in self:
            record.user_count = len(record.user_ids)

    def copy_data(self, default=None):
        new_defaults = {'name': _("%s (copy)") % (self.name)}
        default = dict(new_defaults, **(default or {}))
        return super().copy_data(default)

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
        self.employee_ids = [(6, 0, employees.ids)]

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
