from odoo import api, fields, models

class Job(models.Model):
    _inherit = 'hr.job'
    
    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'job_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'job_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'job_validation_id', string='Validación')
    
    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class InternalIssueValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    job_elaboration_id = fields.Many2one(
        'hr.job', string='Puesto')
    job_review_id = fields.Many2one(
        'hr.job', string='Puesto')
    job_validation_id = fields.Many2one(
        'hr.job', string='Puesto')