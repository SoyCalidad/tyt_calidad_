from odoo import models, fields, api

class Question(models.Model):
    _name = 'tyt_recruitment.question'
    _description = 'tyt_recruitment.question'
    _rec_name = 'text'

    text = fields.Char(string="Pregunta")
    type = fields.Selection([('health', 'Salud'),('job', 'Laboral'),('study', 'Estudio')], string="Tipo") 
    state = fields.Selection([('enable', "Habilitado"),('disable', "Inhabilitado")], default='enable', string="Estado")

class Answer(models.Model):
    _name = 'tyt_recruitment.answer'
    _description = 'tyt_recruitment.answer'
    _rec_name = 'text'

    text = fields.Char(string="Respuesta")

    job_application_id = fields.Many2one('tyt_recruitment.job_application')
    question_id = fields.Many2one('tyt_recruitment.question', string="Pregunta")