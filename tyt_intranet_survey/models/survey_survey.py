from odoo import api, exceptions, fields, models, _


class Survey(models.Model):
    _inherit = 'survey.survey'

    authorized_group_id = fields.Many2one('intranet.groups', string='Authorized Group')
    department_id = fields.Many2one(related='authorized_group_id.department_id', string='Department', store=True)
    job_id = fields.Many2one(related='authorized_group_id.job_id', string='Job Position', store=True,)
    is_published = fields.Boolean('Published', default=False)
    published_date_start = fields.Date('Published Start Date', compute='_compute_published_date_start', readonly=False, store=True)
    published_date_end = fields.Date('Published End Date', store=True)

    @api.depends('is_published')
    def _compute_published_date_start(self):
        for record in self:
            if record.is_published and not record.published_date_start:
                record.published_date_start = fields.Date.today()
