from odoo import models, fields 


class AreaEncuesta(models.Model):
    _name = "tyt_studio.survey_area"
    _description = "Area encuesta"
    _order = "sequence asc, id asc"
    
    name = fields.Char(string="Descripción")
    code = fields.Char(string="code")
    sequence = fields.Integer(string="Secuencia")


class TipoEncuesta(models.Model):
    _name = "tyt_studio.survey_type"
    _description = "Tipo encuesta"
    _order = "sequence asc, id asc"
    
    name = fields.Char(string="Descripción")
    code = fields.Char(string="code")
    sequence = fields.Integer(string="Secuencia")    