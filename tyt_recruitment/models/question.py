from odoo import models, fields, api

class Question(models.Model):
    _name = 'tyt_recruitment.question'
    _description = 'tyt_recruitment.question'
    _rec_name = 'text'
    _inherit = ['mail.thread']

    text = fields.Char(string="Pregunta", tracking=True)
    type = fields.Selection([('health', 'Salud'),('job', 'Laboral'),('study', 'Estudio')], string="Tipo", tracking=True) 
    state = fields.Selection([('enable', "Habilitado"),('disable', "Inhabilitado")], default='enable', string="Estado", tracking=True)

class Answer(models.Model):
    _name = 'tyt_recruitment.answer'
    _description = 'tyt_recruitment.answer'
    _rec_name = 'text'
    _inherit = ['mail.thread']

    text = fields.Char(string="Respuesta", tracking=True)

    job_application_id = fields.Many2one('tyt_recruitment.job_application', tracking=True)
    question_id = fields.Many2one('tyt_recruitment.question', string="Pregunta", tracking=True)