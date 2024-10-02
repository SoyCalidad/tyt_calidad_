from odoo import api, exceptions, fields, models, _


class Survey(models.Model):
    _inherit = 'survey.survey'

    authorized_group_id = fields.Many2one('intranet.groups', string='Authorized Group')
    department_id = fields.Many2one(related='authorized_group_id.department_id', string='Department', store=True)
    job_id = fields.Many2one(related='authorized_group_id.job_id', string='Job Position', store=True)
    sitio_id = fields.Many2one(related='authorized_group_id.sitio_id', string='Site', store=True)
    employee_ids = fields.Many2many(related='authorized_group_id.employee_ids', string='Employees')
    user_ids = fields.Many2many(related='authorized_group_id.user_ids', string='Users')
    published_start_date = fields.Date('Published Start Date', copy=False)
    published_end_date = fields.Date('Published End Date', copy=False)
    is_published = fields.Boolean('Published', default=False, copy=False)
    access_mode = fields.Selection(selection_add=[('intranet', 'Intranet')], ondelete={'intranet': 'cascade'})
