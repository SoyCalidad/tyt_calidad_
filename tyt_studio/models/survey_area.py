from odoo import models, fields 


class AreaEncuesta(models.Model):
    _name = "tyt_studio.survey_area"
    _description = "Area encuesta"
    _order = "sequence asc, id asc"
    
    name = fields.Char(string="Descripción", required=True,translate=True)
    code = fields.Char(string="code")
    sequence = fields.Integer(string="Secuencia")


class TipoEncuesta(models.Model):
    _name = "tyt_studio.survey_type"
    _description = "Tipo encuesta"
    _order = "sequence asc, id asc"
    
    name = fields.Char(string="Descripción", translate=True, required=True)
    code = fields.Char(string="code")
    sequence = fields.Integer(string="Secuencia")    