from odoo import api, exceptions, fields, models, _

import logging 

_logger = logging.getLogger(__name__)

class Survey(models.Model):
    _inherit = 'survey.survey'

    access_mode = fields.Selection(selection_add=[('intranet', 'Intranet')], ondelete={'intranet': 'cascade'})
    questions_mandatory = fields.Boolean('Mandatory Questions', default=False)
    job_id = fields.Many2one('hr.job', string='Job Position', copy=False)
    department_id = fields.Many2one('hr.department', string='Department', copy=False)
    gps = fields.Boolean(string='gps')
    group_ids = fields.Many2many('res.groups', string='Groups', copy=False)
    published_start_date = fields.Date('Published Start Date', copy=False)
    published_end_date = fields.Date('Published End Date', copy=False)
    publish_state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
    ], string='Publish State', default='draft', copy=False)

    @api.onchange('gps')
    def _onchange_gps(self):
        if self.gps and self.job_id:
            groups = self.env['res.groups'].search([('x_studio_job', '=', self.job_id.id)])
            self.group_ids = [(6, 0, groups.ids)] if groups else []
            self.gps = False
