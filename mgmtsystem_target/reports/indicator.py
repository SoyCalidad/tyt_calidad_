from odoo import api, fields, models
from odoo.exceptions import UserError
from collections import defaultdict


class IndicatorReportWizard(models.TransientModel):
    _name = 'indicator.report'
    _description = 'Indicator Report'

    filter_by = fields.Selection([
        ('date', 'Fecha'),
        ('indicator', 'Indicador'),
    ], string='Filtrar por', default='date')

    start_date = fields.Date('Desde')
    end_date = fields.Date('Hasta')

    indicator_ids = fields.Many2many(
        'mgmtsystem.indicator', string='Indicadores')

    def action_print(self):
        if self.filter_by == 'date':
            indicator_ids = self.env['mgmtsystem.indicator'].search([('start_date','>=',self.start_date or '1000-01-01'),('start_date','<=',self.end_date or '9999-12-31')])
        elif self.filter_by == 'indicator':
            indicator_ids = self.indicator_ids
        else:
            raise UserError('Seleccione un filtro')
        return self.env.ref('mgmtsystem_target.action_report_indicators1').report_action(indicator_ids)
