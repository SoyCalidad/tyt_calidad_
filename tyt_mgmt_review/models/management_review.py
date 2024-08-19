from odoo import fields, models, api

class ManagementReview(models.Model):
    _inherit = 'management.review'

    line2_ids = fields.One2many(
        string='Detalles Revisión por la dirección',
        comodel_name='management.review.line2',
        inverse_name='mgmt_review_id',
    )


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

    name = fields.Char(string='Nombre')
    job_id = fields.Many2one(comodel_name='hr.job', string='Puesto')
    clausule_id = fields.Many2one('management.review.line2.clausule', string='Clausula')
    description = fields.Char(string='Descripción')
    process2_id = fields.Many2one('management.review.line2.process', string='Procesos')
    department_pro_id = fields.Many2one('hr.department', string='Área responsable de proceso')
    department_clau_id = fields.Many2one('hr.department', string='Área responsable de clausula')
    achieved = fields.Boolean(string='Cumple')

