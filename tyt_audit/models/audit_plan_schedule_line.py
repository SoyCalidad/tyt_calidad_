from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

'''
class MeasurementPeriod(models.Model):
    _inherit = "mgmtsystem.frequency"
'''

class PlanGeneralScheduleLine(models.Model):
    _name = "audit.plan.schedule.line"
    _description = "Cronograma de Auditoría - General / Cronograma / Fechas"
    _check_company_auto = True

    schedule_id = fields.Many2one(
        string='Linea de Cronograma de Auditoría - General / Cronograma',
        comodel_name='audit.plan.schedule',
        ondelete='cascade',
    )

    name = fields.Char('Subjects', required=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    
    scheduled_date = fields.Date(
        string='Fecha prevista',
    )

    # new field
    done = fields.Boolean(string="Realizado")