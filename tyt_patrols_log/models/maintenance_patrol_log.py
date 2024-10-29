from odoo import api, fields, models


class MaintenancePatrolLog(models.Model):
    """ Modelo para la Bitácora de rondines """

    _name = 'maintenance.patrollog'
    _description = 'Patrol Log'
    
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    name = fields.Char(string='Name', required=True, copy=False, index=True)
    user_id = fields.Many2one('res.users', string='Created by',required=True, default=lambda self: self.env.user)
    production_date = fields.Date(string='Production Date', required=True, default=fields.Date.today)
    observations = fields.Text(string='Observations')
    
    patrol_log_line_ids = fields.One2many(
        'maintenance.patrollog.line', 'patrol_log_id', string='Patrol Lines',
        default=lambda self: [
            {'location': 'Recepción'},
            {'location': 'Salas'},
            {'location': 'Operaciones'},
            {'location': 'Oficinas Administrativas'}, 
            {'location': 'Baños'},
            {'location': 'Loker'}
        ]
    )
    
    patrol_log_stages_ids = fields.One2many(
        'maintenance.patrollog.stage', 'patrol_log_id', string='Stage Manager',
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
        

class MaintenancePatrolLogLine(models.Model):
    """ Línea de la Bitácora de rondines """

    _name = 'maintenance.patrollog.line'
    _description = 'Patrol Log Line'
    
    patrol_log_id = fields.Many2one(
        'maintenance.patrollog', string='Patrol Log', required=True, ondelete='cascade'
    )
    
    location = fields.Char(string='Location', required=True)
    description = fields.Text(string='Description')

class MaintenancePatrolLogStage(models.Model):
    """ Etapas de la Bitácora de rondines """

    _name = 'maintenance.patrollog.stage'
    _description = 'Patrol Log Stage'
    
    patrol_log_id = fields.Many2one(
        'maintenance.patrollog', string='Patrol Log', required=True, ondelete='cascade'
    )
    
    stage = fields.Char(string='Stage', required=True)
    manager_id = fields.Many2one('res.users', string='Manager', required=True)
