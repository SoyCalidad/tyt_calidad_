from odoo import api, fields, models
from odoo.exceptions import UserError

class TrainingDatabaseWizard(models.TransientModel):
    _name = 'training_database.wizard'

    training_filter = fields.Boolean(string='Filtrar por capacitaciones', default=True)
    training_ids = fields.Many2many(
        'mgmtsystem.plan.training', string='Capacitaciones')

    date_filter = fields.Boolean(string='Filtrar por fechas', default=False)
    init_date = fields.Date(string='Fecha inicial')
    end_date = fields.Date(string='Fecha final')

    employee_filter = fields.Boolean(string='Filtrar por empleados', default=False)
    employee_ids = fields.Many2many('hr.employee', string='Empleados')

    @api.onchange('training_filter')
    def _onchange_training_filter(self):
        if self.training_filter:
            self.date_filter = self.employee_filter = False

    @api.onchange('date_filter')
    def _onchange_date_filter(self):
        if self.date_filter:
            self.training_filter = self.employee_filter = False

    @api.onchange('employee_filter')
    def _onchange_employee_filter(self):
        if self.employee_filter:
            self.training_filter = self.date_filter = False

    def action_print(self):
        if self.date_filter:
            query = []
            if self.init_date:
                query.append(('date_training', '>=', self.init_date))
            if self.end_date:
                ('date_training', '<=', self.end_date)
            if query:
                training_ids = self.env['mgmtsystem.plan.training'].search(query)
            else:
                training_ids = None
        else:
            training_ids = self.training_ids
            
        print (training_ids)

        data = self.read()[0]
        datas = {
            'ids': self._ids,
            'docs': training_ids,
            'is_wizard': True,
        }
        if training_ids:
            return self.env.ref('mgmtsystem_employees.report_training_complete_xlsx').report_action(training_ids)
        else:
            raise UserError('No se han encontrado capacitaciones en ese rango de fechas')


class TrainingDatabaseLineWizard(models.TransientModel):
    _name = 'training_database.line.wizard'

    comunication_plan_line_id = fields.Many2one(
        'training_database.line', string='Comunicación')

    def action_print(self):
        data = self.read()[0]
        datas = {
            'ids': self._ids,
            'docs': self.comunication_plan_line_id.id,
            'is_wizard': True,
        }
        res = self.env.ref('mgmtsystem_comunication.action_report_comunication_plan_line').report_action(
            self, data=datas)
        return res
