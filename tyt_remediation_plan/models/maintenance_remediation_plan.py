from odoo import api, fields, models


class MaintenanceRemediationPlan(models.Model):
    """ Modelo para el Plan de remediaciones """

    _name = 'maintenance.remediationplan'
    _description = 'Remediation Plan'
    
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    name = fields.Char(string='Name', required=True, copy=False, index=True)
    user_id = fields.Many2one('res.users', string='Created by',required=True, default=lambda self: self.env.user)
    production_date = fields.Date(string='Production Date', required=True, default=fields.Date.today)
    observations = fields.Text(string='Observations')
    
    remediation_plan_line_ids = fields.One2many(
        'maintenance.remediationplan.line', 'remediation_plan_id', string='Remediation Plan Lines')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string="Status", default='draft')
    
    def action_confirm(self):
        self.ensure_one()
        self.write({'state': 'confirmed'})
        return True

    def action_cancel(self):
        self.ensure_one()
        self.write({'state': 'draft'})
        return {'type': 'ir.actions.act_window_close'}

    def action_draft(self):
        self.write({'state': 'draft'})


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
