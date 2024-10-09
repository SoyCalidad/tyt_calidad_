from odoo import api, fields, models


class MaintenanceRemediationLog(models.Model):
    """ Modelo para la Bitácora de remediaciones """

    _name = 'maintenance.remediationlog'
    _description = 'Remediation Log'
    
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    name = fields.Char(string='Name', required=True, copy=False, index=True)
    user_id = fields.Many2one('res.users', string='Created by',required=True, default=lambda self: self.env.user)
    production_date = fields.Date(string='Production Date', required=True, default=fields.Date.today)
    observations = fields.Text(string='Observations')
    
    remediation_log_line_ids = fields.One2many(
        'maintenance.remediationlog.line', 'remediation_log_id', string='Remediation Lines',
        default=lambda self: [
            {'location': 'Recepcion'},
            {'location': 'Salas'},
            {'location': 'Operaciones'},
            {'location': 'Oficinas Administrativas'}, 
            {'location': 'Baños'},
            {'location': 'Loker'}
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
        

class MaintenanceRemediationLogLine(models.Model):
    """ Línea de la Bitácora de remediaciones """

    _name = 'maintenance.remediationlog.line'
    _description = 'Remediation Log Line'
    
    remediation_log_id = fields.Many2one(
        'maintenance.remediationlog', string='Remediation Log', required=True, ondelete='cascade'
    )
    
    location = fields.Char(string='Location', required=True)
    detection = fields.Char(string='Detection')
    remediation = fields.Char(string='What was done?')
