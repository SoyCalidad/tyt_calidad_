from odoo import fields, models, api

class ManagementReviewTeamLine2(models.Model):
    _name = "management.review.location"
    _description = "Ubicación"

    name = fields.Char(string='Nombre')

class ManagementReview(models.Model):
    _inherit = 'management.review'

    line2_ids = fields.One2many(
        string='Detalles Revisión por la dirección',
        comodel_name='management.review.line2',
        inverse_name='mgmt_review_id',
    )
    
    location_id = fields.Many2one('management.review.location', string='Ubicación')


class ManagementReviewTeamLine2(models.Model):
    _name = "management.review.line2.clausule"
    _description = "Integrante comité de calidad"

    name = fields.Char(string='Nombre')

class ManagementReviewTeamLine2(models.Model):
    _name = "management.review.line2.process"
    _description = "Integrante comité de calidad"

    name = fields.Char(string='Nombre')

class ManagementReviewTeamLine2(models.Model):
    _name = "management.review.line2"
    _description = "Integrante comité de calidad"

    mgmt_review_id = fields.Many2one('management.review', string='Revisión por la dirección')

    name = fields.Many2one('hr.employee', string='Nombre')
    job_id = fields.Many2one('hr.job', string='Puesto', related='name.job_id', readonly=True, store=True)

    clausule_id = fields.Many2one('management.review.line2.clausule', string='Clausula')
    description = fields.Char(string='Descripción')
    process2_id = fields.Many2one('management.review.line2.process', string='Procesos')
    department_pro_id = fields.Many2one('hr.department', string='Área responsable de proceso')
    department_clau_id = fields.Many2one('hr.department', string='Área responsable de clausula')
    achieved = fields.Boolean(string='Cumple')

