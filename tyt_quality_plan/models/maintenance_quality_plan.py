from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class MaintenanceQualityPlan(models.Model):
    """ Modelo para el Plan de Calidad """

    _name = 'maintenance.qualityplan'
    _description = 'Quality Plan'
    
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    name = fields.Char(string='Name', required=True, copy=False, index=True)
    week = fields.Integer(string='Week', required=True)
    site = fields.Many2one('tyt_studio.sites', string='Site', required=True)
    
    total_controls = fields.Integer(string='Total Controls', compute='_compute_totals', store=True)
    total_monitoring = fields.Integer(string='Total Monitoring', compute='_compute_totals', store=True)
    total_percentage = fields.Float(string='Total Percentage', compute='_compute_totals', store=True)
    
    observations = fields.Text(string='Observations')
    
    quality_plan_line_ids = fields.One2many(
        'maintenance.qualityplan.line', 'quality_plan_id', string='Quality Plan Lines')
    
    quality_plan_stages_ids = fields.One2many(
        'maintenance.qualityplan.stage', 'quality_plan_id', string='Stage Manager',
        default=lambda self: [
            {'stage': 'Elaboración'},
            {'stage': 'Revisión'},
            {'stage': 'Validación'}
        ]
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string="Status", default='draft')
    
    @api.depends('quality_plan_line_ids')
    def _compute_totals(self):
        """Suma la cantidad de controles, monitoreos y porcentajes de las líneas del plan"""
        for plan in self:
            total_controls = 0
            total_monitoring = 0
            total_percentage = 0.0
            
            for line in plan.quality_plan_line_ids:
                total_controls += 1 if line.control else 0
                total_monitoring += 1 if line.monitoring else 0
                total_percentage += line.percentage

            plan.total_controls = total_controls
            plan.total_monitoring = total_monitoring
            plan.total_percentage = total_percentage

            if total_percentage > 100:
                raise ValidationError(_("The total percentage cannot exceed 100%. Please review the plan lines."))


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


class MaintenanceQualityPlanLine(models.Model):
    """ Línea del Plan de Calidad """

    _name = 'maintenance.qualityplan.line'
    _description = 'Quality Plan Line'
    
    quality_plan_id = fields.Many2one(
        'maintenance.qualityplan', string='Quality Plan', required=True, ondelete='cascade'
    )
    
    control = fields.Text(string='Control', required=True)
    monitoring = fields.Text(string='Monitoring', required=True)
    percentage = fields.Float(string='Percentage', required=True)
    status = fields.Selection([
        ('Cumple', 'CUMPLE'),
        ('No Cumple', 'NO CUMPLE'),
    ], string="Status", default='Cumple')

class MaintenanceQualityLogStage(models.Model):
    """ Etapas de la Bitácora de rondines """

    _name = 'maintenance.qualityplan.stage'
    _description = 'Quality Log Stage'
    
    quality_plan_id = fields.Many2one(
        'maintenance.qualityplan', string='Quality Log', required=True, ondelete='cascade'
    )
    
    stage = fields.Char(string='Stage', required=True)
    manager_id = fields.Many2one('res.users', string='Manager', required=True)
