from odoo import models, fields, api

class Expedient(models.Model):
    _name = 'tyt_recruitment.expedient'
    _description = 'tyt_recruitment.expedient'
    _rec_name = 'success_rate'

    success_rate = fields.Float(string="Estatus del expediente", digits=(5, 2), default=0)
    
    birth_certificate = fields.Many2one('tyt_recruitment.expedient_file', string="Acta de nacimiento")
    rfc = fields.Many2one('tyt_recruitment.expedient_file', string="RFC")
    curp = fields.Many2one('tyt_recruitment.expedient_file', string="CURP")
    study_certificate = fields.Many2one('tyt_recruitment.expedient_file', string="Comprobante de estudio")
    proposed_letter = fields.Many2one('tyt_recruitment.expedient_file', string="Carta propuesta")
    ine = fields.Many2one('tyt_recruitment.expedient_file', string="INE")
    reference_validation = fields.Many2one('tyt_recruitment.expedient_file', string="Validación de referencias")
    health_survey = fields.Many2one('tyt_recruitment.expedient_file', string="Encuesta de salud")
    job_application = fields.Many2one('tyt_recruitment.expedient_file', string="Solicitud de empleo")
    utility_bill = fields.Many2one('tyt_recruitment.expedient_file', string="Comprobante de domicilio")
    psychometric = fields.Many2one('tyt_recruitment.expedient_file', string="Psicométrico")
    snn = fields.Many2one('tyt_recruitment.expedient_file', string="SNN")
    interbank_key = fields.Many2one('tyt_recruitment.expedient_file', string="Clave interbancaria")
    value_proposition = fields.Many2one('tyt_recruitment.expedient_file', string="Propuesta de valor")

class ExpedientFile(models.Model):
    _name = 'tyt_recruitment.expedient_file'
    _description = 'tyt_recruitment.expedient_file'
    _rec_name = 'title'

    title = fields.Char(string="Respuesta")
    file = fields.Binary(string="Archivo")
    state = fields.Selection([
        ('loaded', 'Cargado'),
        ('pending', 'Pendiente')
    ], string="Estatus")
    approved = fields.Selection([
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado')
    ], string="Aprobación")