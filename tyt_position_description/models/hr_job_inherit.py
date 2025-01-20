from odoo import models, fields


class HrJobWorkday(models.Model):
    _name = 'hr.job.work_day'
    _description = "hr.job.work_day"

    name = fields.Integer()


class HrJob(models.Model):
    _inherit = 'hr.job'

    ## jobs ##
    functional_head = fields.Many2one('res.partner', string='Jefe funcional')

    adm_head = fields.Many2one('res.partner', string='Jefe administrativo')

    hr_job_work_day_id = fields.Many2one('hr.job.work_day', string='Jornada')