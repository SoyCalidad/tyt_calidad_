from odoo import _, api, fields, models


class Employee(models.Model):
    _inherit = 'hr.employee'

    process_ids = fields.Many2many(
        comodel_name='mgmt.process', string='Procedimientos', domain=[('active','=',True)])
    process_count = fields.Integer(
        string='Procedimientos', compute='get_process_count')

    training_ids = fields.Many2many(
        string=u'Capacitaciones',
        comodel_name='mgmtsystem.plan.training',
        relation='employee_training_rel',
        column1='training_id',
        column2='employee_id',
    )
    trainings_count = fields.Integer(
        string='Capacitaciones', compute='get_trainings_count')

    meeting_ids = fields.Many2many(
        string=u'Reuniones',
        comodel_name='record.meeting',
        relation='employee_record_rel',
        column1='record_id',
        column2='employee_id',
    )
    meetings_count = fields.Integer(
        string='Reuniones', compute='get_meetings_count')

    @api.depends('process_ids')
    def get_process_count(self):
        for each in self:
            if each.process_ids:
                each.process_count = len(each.process_ids)
            else:
                each.process_count = 0

    @api.depends('training_ids')
    def get_trainings_count(self):
        for each in self:
            if each.training_ids:
                each.trainings_count = len(each.training_ids)
            else:
                each.trainings_count = 0

    @api.depends('meeting_ids')
    def get_meetings_count(self):
        for each in self:
            if each.meeting_ids:
                each.meetings_count = len(each.meeting_ids)
            else:
                each.meetings_count = 0

    def open_process_view(self):
        ids = [x.id for x in self.process_ids]
        result = self.env.ref(
            'mgmtsystem_process.action_mgmt_procedures').sudo().read()[0]
        result['domain'] = [('id', 'in', ids)]
        return result

    def open_training_view(self):
        ids = [x.id for x in self.training_ids]
        result = self.env.ref(
            'mgmtsystem_employees.hr_item_training_action').read()[0]
        result['domain'] = [('id', 'in', ids)]
        return result

    def open_meeting_view(self):
        ids = [x.id for x in self.meeting_ids]
        result = self.env.ref(
            'mgmtsystem_comunication.record_meeting_action').sudo().read()[0]
        result['domain'] = [('id', 'in', ids)]
        return result


class Process(models.Model):
    _inherit = 'mgmt.process'

    employee_ids = fields.Many2many(
        comodel_name='hr.employee', string='Empleados')
    employees_count = fields.Integer(
        string='Empleados', compute='get_employees_count'
    )

    @api.depends('employee_ids')
    def get_employees_count(self):
        for each in self:
            if each.employee_ids:
                each.employees_count = len(each.employee_ids)
            else:
                each.employees_count = 0

    def open_employee_view(self):
        ids = [x.id for x in self.employee_ids]
        result = self.env.ref(
            'hr.open_view_employee_list_my').read()[0]
        result['domain'] = [('id', 'in', ids)]
        return result
