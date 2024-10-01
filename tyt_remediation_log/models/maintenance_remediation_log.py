from odoo import api, fields, models


class MaintenanceRemediationLog(models.Model):
    """ Modelo para la Bitácora de remediaciones """

    _name = 'maintenance.remediationlog'
    _description = 'Remediation Log'
    
    name = fields.Char(string='Name', required=True, copy=False, index=True)
    user_id = fields.Many2one('res.users', string='Created by',required=True, default=lambda self: self.env.user)
    production_date = fields.Date(string='Production Date', required=True, default=fields.Date.today)
    observations = fields.Text(string='Observations')
    
    remediation_log_line_ids = fields.One2many(
        'maintenance.remediationlog.line', 'remediation_log_id', string='Remediation Lines',
        default=lambda self: [
            {'location': 'Reception'},
            {'location': 'Halls'},
            {'location': 'Operations'},
            {'location': 'Administrative Offices'},
            {'location': 'Bathrooms'},
            {'location': 'Loker'}
        ]
    )
    
    def action_save(self):
        self.ensure_one()  
        return True

    def action_cancel(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}


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
