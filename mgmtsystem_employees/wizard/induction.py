from odoo import api, fields, models


class InductionWizard(models.TransientModel):
    _name = 'employee_induction.wizard'

    company_id = fields.Many2one(
        string=u'Compañia',
        comodel_name='res.company', required=True,
        domain=lambda self: [('id', 'in', self.env.user.company_ids.ids)],
        default=lambda self: self.env.user.company_id.id,
    )

    employee_ids = fields.Many2many('hr.employee', string='Empleados')

    def action_print(self):
        return self.env.ref('mgmtsystem_employees.action_report_employee_induction').report_action(self.employee_ids)

    