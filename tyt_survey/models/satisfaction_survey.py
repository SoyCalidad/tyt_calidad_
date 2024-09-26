from odoo import fields, models


class SurveySatisfaction(models.Model):
    _name = "tyt.satisfaction.survey"
    _description = "Satisfaction Survey"

    name = fields.Char(string="Name", required=True)
