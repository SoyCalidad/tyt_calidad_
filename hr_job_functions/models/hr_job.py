from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
import base64
import tempfile


class Job(models.Model):
    _name = 'hr.job'
    _inherit = ['hr.job', 'mgmtsystem.validation.hr.job',
                'mail.thread', 'mail.activity.mixin']

    parent_id = fields.Many2one('hr.job', string='Cargo jefe inmediato')
    functions = fields.One2many(
        'hr.job.function', 'job_id', string='Funciones Generales', copy=True)
    evaluation_factors = fields.One2many(
        'hr.job.evaluation_factor', 'job_id', string='Factores de Evaluación', copy=True)
    coordinators = fields.One2many(
        'hr.job.coordinator', 'job_id', string='Coordinadores', copy=True)
    supervisors = fields.One2many(
        'hr.job.supervisor', 'job_id', string='Supervisores', copy=True)
    superviseds = fields.One2many(
        'hr.job.supervised', 'job_id', string='Supervisados', copy=True)
    job_profile = fields.Many2one('hr.job.profile', string='Perfil del puesto')
    generic_skills = fields.One2many(
        'hr.job.generic_skill', 'job_id', string='Competencias Genéricas', copy=True)
    workteam_skills = fields.One2many(
        'hr.job.workteam_skill', 'job_id', string='Competencias de Trabajo en Equipo', copy=True)
    personal_skills = fields.One2many(
        'hr.job.personal_skill', 'job_id', string='Competencias Personales', copy=True)
    strategic_skills = fields.One2many(
        'hr.job.strategic_skill', 'job_id', string='Competencias Estratégicas', copy=True)
    active = fields.Boolean('Active', default=True)

    
    state = fields.Selection([
        ('a', 'Contratación en curso'),
        ('b', 'No seleccionado'),
    ], string='Estado')
    
    # Remove the uniqueness rule to allow duplicate names
    _sql_constraints = [
        ('name_company_uniq', 'unique(company_id, department_id)', 'The name of the job position must not be unique per department in company!'),
        ('no_of_recruitment_positive', 'CHECK(no_of_recruitment >= 0)', 'The expected number of new employees must be positive.'),
    ]    

    # Update copy method
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = self.name  # Mantener el mismo nombre y Evitar que se agregue "(copy)" al nombre
        return super(Job, self).copy(default=default)


    validation_state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('cancel', 'Obsoleto')
        ],
        default='elaborate',
        copy=False,
    )
    process_id = fields.Many2one(
        'mgmt.process', string='Proceso', required=False, domain=[('active','=',True)])
    parent_edition = fields.Many2one(
        comodel_name='hr.job', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='hr.job', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    employee_qty = fields.Integer(
        compute='_compute_employee_qty', string='Empleados')

    @api.depends('employee_ids')
    def _compute_employee_qty(self):
        for each in self:
            each.employee_qty = len(each.employee_ids)

    def open_employees(self):
        ids = [x.id for x in self.employee_ids]
        result = self.env.ref('hr.open_view_employee_list_my').read()[0]
        result['domain'] = [('id', 'in', ids)]
        return result

    def write(self, values):
        result = super(Job, self).write(values)
        return result

    def create_action(self, vuser_id):
        action = self.env.ref('hola_calidad.p_mail_activity_action').read()[0]
        print(self._name)
        self.env.cr.execute("""SELECT id FROM ir_model 
                          WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        action['context'] = {
            'default_res_id': self.ids[0],
            'default_res_model': self._name,
            'default_res_model_id': model_id,
            'default_user_id': vuser_id,
        }
        return action

    def cancel_other_versions(self):
        """Cancela las versiones anteriores"""
        for each in self:
            for version in each.old_versions:
                version.write({
                    'validation_state': 'cancel'
                })

    def send_elaborate(self):
        if not self.elaboration_step:
            raise ValidationError('Ingrese los usuarios para la Elaboración')
        self.write({'validation_state': 'elaborate'})

    def send_review(self):
        if not self.review_step:
            raise ValidationError('Ingrese los usuarios para la Revisión')
        if not self.elaboration_users_check:
            raise ValidationError(
                'La elaboración no ha sido aprobada por los usuarios asignados')
        self.write({
            'validation_state': 'review',
        })

    def send_validate(self):
        if not self.validation_step:
            raise ValidationError('Ingrese los usuarios para la validación')
        if not self.review_users_check:
            raise ValidationError(
                'La revisión no ha sido aprobada por los usuarios asignados')
        self.write({
            'validation_state': 'validate',
        })

    def send_validate_ok2(self):
        if not self.validation_users_check:
            raise ValidationError(
                'La validación no ha sido aprobada por los usuarios asignados')
        self.cancel_other_versions()
        self.write({
            'validation_state': 'validate_ok',
        })

    def send_cancel(self):
        self.write({'validation_state': 'cancel'})

    def action_open_older_versions(self):
        result = self.env.ref(
            'hr_job_functions.hr_job_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def notify_employee_email(self):
        self.ensure_one()
        sender = self.env.company.email
        for each in self.employee_ids:
            date = datetime.now().strftime('%d/%m/%Y')
            body = 'Manual de organización y funciones'
            fp = tempfile.NamedTemporaryFile(suffix='.pdf')
            data, data_format = self.env.ref(
                'hr_job_functions.report_funinings').render([self.id])
            fp.write(data)
            part = open(fp.name, 'rb').read()
            attachment = self.env['ir.attachment'].create({
                'datas': base64.b64encode(part),
                'name': 'Manual de organización y funciones.pdf'})
            template_data = {
                'subject': "Manual de funciones %s" % date,
                'body_html': body,
                'email_from': sender,
                'email_to': each.work_email,
                'attachment_ids': [(4, attachment.id)]
            }
            self.env['mail.mail'].create(template_data).send()


class JobFunctions(models.Model):
    _name = 'hr.job.function'

    name = fields.Text(string='Descripción')
    job_id = fields.Many2one('hr.job', string='Posición')
    sequence = fields.Char(string='Secuencia')


class EvaluationFactors(models.Model):
    _name = 'hr.job.evaluation_factor'

    name = fields.Text(string='Descripción')
    job_id = fields.Many2one('hr.job', string='Posición')


class JobCoordinator(models.Model):
    _name = 'hr.job.coordinator'

    related_job = fields.Many2one('hr.job', string='Posición')
    job_id = fields.Many2one('hr.job', string='Posición')


class JobSupervisor(models.Model):
    _name = 'hr.job.supervisor'

    related_job = fields.Many2one('hr.job', string='Posición')
    job_id = fields.Many2one('hr.job', string='Posición')


class JobSupervised(models.Model):
    _name = 'hr.job.supervised'

    related_job = fields.Many2one('hr.job', string='Posición')
    job_id = fields.Many2one('hr.job', string='Posición')


class JobProfile(models.Model):
    _name = 'hr.job.profile'

    name = fields.Char(string='Nombre', required=True)
    degree = fields.Selection([
        ('none', 'Sin estudios'),
        ('elementary', 'Primaria completa'),
        ('high_school', 'Secundaria completa'),
        ('college', 'Superior'),
        ('master', 'Maestría'),
        ('doctor', 'Doctorado')
    ], string='Grado académico')
    specialties = fields.One2many(
        'hr.job.profile.specialty', 'profile_id', string='Especialidades')
    exprience = fields.One2many(
        'hr.job.profile.experience', 'profile_id', string='Experiencia')


class JobProfileSpecialty(models.Model):
    _name = 'hr.job.profile.specialty'

    name = fields.Char(string='Descripción')
    profile_id = fields.Many2one('hr.job.profile', string='Perfil')


class JobProfileExperience(models.Model):
    _name = 'hr.job.profile.experience'

    name = fields.Char(string='Descripción')
    profile_id = fields.Many2one('hr.job.profile', string='Perfil')


class Skill(models.Model):
    _name = 'hr.job.skill'

    job_id = fields.Many2one('hr.job', string='Posición')
    name = fields.Text(string='Descripción')
    relevance = fields.Selection([
        ('medium', 'Mediana'),
        ('high', 'Alta'),
        ('highest', 'Muy alta')
    ], string='Nivel de relevancia')


class GenericSkill(models.Model):
    _inherit = 'hr.job.skill'
    _name = 'hr.job.generic_skill'


class WorkteamSkill(models.Model):
    _inherit = 'hr.job.skill'
    _name = 'hr.job.workteam_skill'


class PersonalSkill(models.Model):
    _inherit = 'hr.job.skill'
    _name = 'hr.job.personal_skill'


class StrategicSkill(models.Model):
    _inherit = 'hr.job.skill'
    _name = 'hr.job.strategic_skill'
