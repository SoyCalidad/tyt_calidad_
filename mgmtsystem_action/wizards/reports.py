from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


class ActionActionReportWizard(models.TransientModel):
    _name = 'action.action_report.wizard'

    action_ids = fields.Many2many(
        'mgmtsystem.action',
        string='Acciones',
    )
    init_date = fields.Date(string='Fecha inicial')
    end_date = fields.Date(string='Fecha final')

    filter_by = fields.Selection([
        ('date', 'Por fecha'),
        ('action', 'Acciones'),
    ], string='Filtrar por', default='date')

    def print_action_report(self):
        if self.filter_by == 'date':
            if self.init_date and self.end_date:
                init_date = datetime.combine(
                    self.init_date, datetime.min.time())
                end_date = datetime.combine(self.end_date, datetime.max.time())
                ids = self.env['mgmtsystem.action'].search(
                    [('date_open', '>=', init_date), ('date_open', '<=', end_date)]).ids
            else:
                raise UserError('Ingrese el rango de fechas')
        elif self.filter_by == 'action':
            ids = self.action_ids.ids
        else:
            raise UserError('Selecciona un filtro')
        if ids:
            return self.env.ref('mgmtsystem_action.action_report_action').report_action(ids)

    def print_action_report_xls(self):
        if self.filter_by == 'date':
            if self.init_date and self.end_date:
                init_date = datetime.combine(
                    self.init_date, datetime.min.time())
                end_date = datetime.combine(self.end_date, datetime.max.time())
                ids = self.env['mgmtsystem.action'].search(
                    [('date_open', '>=', init_date), ('date_open', '<=', end_date)]).ids
            else:
                raise UserError('Ingrese el rango de fechas')
        elif self.filter_by == 'action':
            ids = self.action_ids.ids
        else:
            raise UserError('Selecciona un filtro')
        if ids:
            return self.env.ref('mgmtsystem_action.action_report_action_xls').report_action(ids)
