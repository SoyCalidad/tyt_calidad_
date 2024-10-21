from odoo import models, fields

class JobApplication(models.Model):
    _name = 'tyt_recruitment.job_application'
    _description = 'tyt_recruitment.job_application'
    _rec_name = 'id'

    request_date = fields.Date(string='Fecha')
    requisition = fields.Char(string='Requisición')
    site = fields.Char(string='Sitio')

    campaign_id = fields.Many2one('tyt_recruitment.campaign', string="Campaña")
    applicant_id = fields.Many2one('tyt_recruitment.applicant')

    # Respuestas de questionario
    answer_ids = fields.One2many('tyt_recruitment.answer', 'job_application_id', string="Respuestas")

class Applicant(models.Model):
    _name = 'tyt_recruitment.applicant'
    _description = 'tyt_recruitment.applicant'
    
    reference = fields.Char(string="Medio")
    name = fields.Char(string="Nombre")
    last_name_father = fields.Char(string="Apellido Paterno")
    last_name_mother = fields.Char(string="Apellido Materno")
    birthplace = fields.Char(string="Lugar de Nacimiento")
    birthdate = fields.Date(string="Fecha de Nacimiento")
    nationality = fields.Char(string="Nacionalidad")
    gender = fields.Selection([
        ('male', 'Masculino'),
        ('female', 'Femenino'),
        ('other', 'Otro'),
    ], string="Género")
    age = fields.Integer(string="Edad")
    marital_status = fields.Selection([
        ('single', 'Soltero/a'),
        ('married', 'Casado/a'),
        ('divorced', 'Divorciado/a'),
        ('widowed', 'Viudo/a'),
    ], string="Estado Civil")
    social_security_number = fields.Char(string="Número de Seguro Social")
    rfc = fields.Char(string="RFC")
    curp = fields.Char(string="CURP")
    address_street = fields.Char(string="Calle y Número")
    address_neighborhood = fields.Char(string="Colonia")
    address_city = fields.Char(string="Municipio")
    number_phone = fields.Char(string="Número de teléfono")
    personal_email = fields.Char(string="Correo electrónico")
    live_with = fields.Char(string="Con quién vive")
    rent_amount = fields.Float(string="Monto semanal de renta")
    infonavit_credit_amount = fields.Float(string="Monto semanal de Infonavit")
    transports = fields.Char(string="Cantidad de transportes y Tiempo de traslado")
    requested_job_position = fields.Char(string="Puesto que solicita")
    monthly_expenses = fields.Float(string="Gastos mensuales aproximados")
    availability = fields.Char(string="Disponibilidad para empezar a trabajar")
    dependents = fields.Char(string="Personas que dependen de ti")
    foreign_nationality = fields.Boolean(string="Cuenta con nacionalidad extranjera")
    daily_activities = fields.Text(string="Describa sus actividades diarias")

    # Relación Many2one con los datos familiares
    father_data_id = fields.Many2one('tyt_recruitment.family_data_detail', string="Datos del padre")
    mother_data_id = fields.Many2one('tyt_recruitment.family_data_detail', string="Datos de la madre")
    spouse_data_id = fields.Many2one('tyt_recruitment.family_data_detail', string="Datos del cónyuge")

    # Relación One2many para los hijos
    children_ids = fields.One2many('tyt_recruitment.child', 'applicant_id', string="Hijos")

    # Campaña
    campaign_id = fields.Many2one('tyt_recruitment.campaign', string="Campaña")

class FamilyDataDetail(models.Model):
    _name = 'tyt_recruitment.family_data_detail'
    _description = 'tyt_recruitment.family_data_detail'

    type = fields.Char(string="Tipo")
    name = fields.Char(string="Nombre")
    occupation = fields.Char(string="Ocupación")

class Child(models.Model):
    _name = 'tyt_recruitment.child'
    _description = 'tyt_recruitment.child'

    name = fields.Char(string="Nombre")
    age = fields.Char(string="Edad") 

    # Relación Many2one con Applicant
    applicant_id = fields.Many2one('tyt_recruitment.applicant', string="Aplicante")