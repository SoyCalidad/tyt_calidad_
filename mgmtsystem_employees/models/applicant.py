from odoo import _, api, fields, models
from datetime import datetime, timedelta


class Applicant(models.Model):
    _inherit = 'hr.applicant'
    
    birthdate = fields.Date(
        string='Fecha de nacimiento',
    )

    age = fields.Integer(
        string='Edad', 
        compute='_compute_age',)

    @api.depends('birthdate')
    def _compute_age(self):
        for record in self:
            if record.birthdate and record.birthdate <= fields.Date.today():
                d1 = record.birthdate
                d2 = datetime.today().date()
                record.age = (d2 - d1).days/365
            else:
                record.age = 0

    genre = fields.Selection([
        ('female', 'Femenino'),
        ('male', 'Masculino'),
        ('both', 'Indistinto')
    ], string='Género')
    
    turn_id = fields.Many2one('hr.applicant.turn', string='Turno')
    
    journal = fields.Selection([
        ('part-time', 'Medio tiempo'),
        ('full-time', 'Tiempo completo'),
    ], string='Jornada')

    requested_by = fields.Many2one('res.users', string='Solicitado por')
    approved_by = fields.Many2one('res.users', string='Aprobado por')
    responsable_id = fields.Many2one('res.users', string='Responsable del seguimiento')

    @api.onchange('job_id')
    def _onchange_job_id(self):
        if self.job_id:
            self.name = 'Solicitud: '+self.job_id.name


class ApplicantTurn(models.Model):
    _name = 'hr.applicant.turn'
    
    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')

class Attachment(models.Model):
    _inherit = 'ir.attachment'

    origin_link = fields.Html(
        string='Link del origen',
        compute='_compute_origin_link',
    )

    @api.depends('res_model','res_id')
    def _compute_origin_link(self):
        for record in self:
            if not record.res_id and record.res_model:
                record.origin_link = ""
            record.origin_link = ("<a data-oe-id=%s data-oe-model='%s' href=#id=%s&model=%s>%s</a>") % (record.res_id, record.res_model, record.res_id, record.res_model, "Ir a origen")