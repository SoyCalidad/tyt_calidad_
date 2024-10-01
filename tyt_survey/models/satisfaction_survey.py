from odoo import fields, models

class SurveySatisfactionQuestion(models.Model):
    _name = "tyt.satisfaction.survey.question"
    _description = "Satisfaction Survey Question"
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

class SurveySatisfactionQuestion(models.Model):
    _name = "tyt.satisfaction.survey.line"
    _description = "Satisfaction Survey Line"
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    text = fields.Text(string="Text")
    qualification = fields.Integer(string="Qualification")
    
    survey_id = fields.Many2one("tyt.satisfaction.survey", string="Survey")

class SurveySatisfaction(models.Model):
    _name = "tyt.satisfaction.survey"
    _description = "Satisfaction Survey"
    _rec_name = "partner_name"

    partner_name = fields.Char(string="Name", required=True)
    job = fields.Char(string="Job", required=True)
    email = fields.Char(string="Email", required=True)
    partner_company = fields.Char(string="Partner", required=True)
    campaign = fields.Char(string="Campaign", required=True)
    
    line_ids = fields.One2many("tyt.satisfaction.survey.line", "survey_id", string="Questions")