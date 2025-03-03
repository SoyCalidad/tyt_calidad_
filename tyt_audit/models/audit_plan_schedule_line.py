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

    name = fields.Char('Subjects')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    
    scheduled_date = fields.Date(
        string='Fecha prevista',
    )
    scheduled_date_is_sunday = fields.Boolean(
        string="Fecha prevista es domingo",
        compute="_compute_scheduled_date_is_sunday",
    )

    # new field
    done = fields.Boolean(string="Realizado")
    auditor_check = fields.Boolean(string='Auditor')
    can_edit_auditor_check = fields.Boolean('Can Edit Auditor', compute='_compute_can_edit_auditor_check')
    fixed_date_check = fields.Boolean(string='Fecha fija')

    def _compute_can_edit_auditor_check(self):
        for record in self:
            record.can_edit_auditor_check = self.env.user.has_group('tyt_audit.group_audit_auditor')

    @api.depends('scheduled_date')
    def _compute_scheduled_date_is_sunday(self):
        for record in self:
            record.scheduled_date_is_sunday = record.scheduled_date and record.scheduled_date.weekday() == 6
