from odoo import models, fields, api, exceptions


class Line(models.Model):
    _inherit = "matrix.block.line"

    stakeholder_id = fields.Many2one(comodel_name="mgmtsystem.stakeholder", string="Parte interesada")
    risk_origin = fields.Char(string="Fuente del Riesgo")
    hr_job_id = fields.Many2many(comodel_name="hr.job", string="Responsable")