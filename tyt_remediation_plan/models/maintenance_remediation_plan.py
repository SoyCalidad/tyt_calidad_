from odoo import api, fields, models


class MaintenanceRemediationPlan(models.Model):
    """ Modelo para el Plan de remediaciones """

    _name = 'maintenance.remediationplan'
    _description = 'Remediation Plan'
    
    name = fields.Char(string='Name', required=True, copy=False, index=True)
    user_id = fields.Many2one('res.users', string='Created by',required=True, default=lambda self: self.env.user)
    production_date = fields.Date(string='Production Date', required=True, default=fields.Date.today)
    observations = fields.Text(string='Observations')
    
    remediation_plan_line_ids = fields.One2many(
        'maintenance.remediationplan.line', 'remediation_plan_id', string='Remediation Plan Lines')
    
    def action_save(self):
        self.ensure_one()  
        return True

    def action_cancel(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}


class MaintenanceRemediationPlanLine(models.Model):
    """ Línea del Plan de remediaciones """

    _name = 'maintenance.remediationplan.line'
    _description = 'Remediation Plan Line'
    
    remediation_plan_id = fields.Many2one(
        'maintenance.remediationplan', string='Remediation Plan', required=True, ondelete='cascade'
    )
    
    remediation_area = fields.Char(string='Remediation Area', required=True)
    activity = fields.Char(string='Activity')
    execution_priority = fields.Float(string='Execution Priority')
    execution_date = fields.Date(string='Execution Date')
    evidence = fields.Char(string='Evidence')
    resourses = fields.Char(string='Resourses')
