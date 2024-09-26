from odoo import api, exceptions, fields, models, _


class Survey(models.Model):
    _inherit = 'survey.survey'

    criteria_id = fields.Many2one('intranet.criteria', string='Criterio de visibilidad')

    department_id = fields.Many2one(related='criteria_id.department_id', string='Departamento', store=True)
    job_id = fields.Many2one(related='criteria_id.job_id', string='Puesto de trabajo', store=True,)

    is_published = fields.Boolean('Publicado', default=False)
    published_date = fields.Date('Fecha de publicación', compute='_compute_published_date', readonly=False, store=True)
    to_date = fields.Date('Fecha de finalización', readonly=False, store=True)

    @api.depends('is_published')
    def _compute_published_date(self):
        for record in self:
            if record.is_published and not record.published_date:
                record.published_date = fields.Datetime.now()
