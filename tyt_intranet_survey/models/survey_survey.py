from odoo import api, exceptions, fields, models, _


class Survey(models.Model):
    _inherit = 'survey.survey'

    authorized_group_id = fields.Many2one('intranet.groups', string='Authorized Group')
    department_id = fields.Many2one(related='authorized_group_id.department_id', string='Department', store=True)
    job_id = fields.Many2one(related='authorized_group_id.job_id', string='Job Position', store=True,)
    published_start_date = fields.Date('Published Start Date')
    published_end_date = fields.Date('Published End Date')
    is_published = fields.Boolean('Published', default=False)
