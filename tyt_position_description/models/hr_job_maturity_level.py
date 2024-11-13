from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class HrJobMarurityLevel(models.Model):
    _name = 'hr.job.maturity.level'
    _description = "Niveles de Madurez"

    name = fields.Char()

    # Puestos que tienen este nivel de Madurez
    job_ids = fields.One2many('hr.job','maturity_level_id', string='Puestos')

class HrJobMaruritySchooling(models.Model):
    _name = 'hr.job.maturity.schooling'
    _description = "Madurez / Escolaridad"

    name = fields.Char(string="Nombre")
    #minimum_age = fields.Integer(string="Edad mínima")
    #language = fields.Char(string="Idioma")


class HrJobMarurityCourses(models.Model):
    _name = 'hr.job.maturity.courses'
    _description = "Madurez / Cursos"

    name = fields.Char(string="Nombre")


class HrJobMarurity(models.Model):
    _name = 'hr.job.maturity'
    _description = "Madurez"

    name = fields.Char()

    job_id = fields.Many2one('hr.job', string='Puesto')
    level_id = fields.Many2one('hr.job.maturity.level', string='Nivel de Madurez')


    graduation_time = fields.Char(string="Tiempo de graduación")

    currency_id = fields.Many2one(
        'res.currency', 
        string='Moneda', 
        required=True, 
        default=lambda self: self.env.company.currency_id
    )

    fixed_salary = fields.Monetary(
        string="Salario Fijo",
        currency_field='currency_id'
    )
    variable_salary = fields.Float(string="Salario Variable", digits=(6, 2))

    full_salary = fields.Monetary(
        string="Salario Integral",
        compute='_compute_full_salary',
        store=True,
        currency_field='currency_id'
    )


    vacancy_ratio = fields.Float(string="Ratio por vacante")

    direct_staff = fields.Integer(string="Personal directo")

    indirect_staff = fields.Integer(string="Personal indirecto")

    schooling_id = fields.Many2one('hr.job.maturity.schooling', string='Jefe funcional')

    minimum_age = fields.Integer(string="Edad mínima")
    language = fields.Char(string="Idioma")

    courses_ids = fields.Many2many(comodel_name='hr.job.maturity.courses', string="Cursos")

    @api.depends('fixed_salary', 'variable_salary')
    def _compute_full_salary(self):
        for record in self:
            if record.fixed_salary and record.variable_salary:
                # Suponiendo que variable_salary es un decimal (ej. 0.05 para 5%)
                record.full_salary = record.fixed_salary + (record.fixed_salary * record.variable_salary)
                
                # Si variable_salary es un entero representando el porcentaje (ej. 5 para 5%)
                # Descomenta la siguiente línea y comenta la anterior
                # record.full_salary = record.fixed_salary + (record.fixed_salary * (record.variable_salary / 100))
            elif record.fixed_salary:
                record.full_salary = record.fixed_salary
            else:
                record.full_salary = 0.0


    @api.constrains('fixed_salary')
    def _check_salaries_positive(self):
        for record in self:
            if record.fixed_salary < 0:
                raise ValidationError("El Salario Fijo no puede ser negativo.")

    @api.constrains('variable_salary')
    def _check_variable_salary(self):
        for record in self:
            # Si variable_salary es un decimal
            if not (0.0 <= record.variable_salary <= 1.0):
                raise ValidationError("El Salario Variable debe estar entre 0% y 100% (0.0 a 1.0).")
            

    @api.depends('maturity_level_id', 'maturity_ids')
    def _compute_maturity_data(self):
        for job in self:
            if job.maturity_level_id:
                maturity = job.maturity_ids.filtered(lambda m: m.level_id == job.maturity_level_id)
                if maturity:
                    job.maturity_data_id = maturity[0]
                else:
                    # Opcional: Crear automáticamente el registro de madurez si no existe
                    maturity = self.env['hr.job.maturity'].create({
                        'job_id': job.id,
                        'level_id': job.maturity_level_id.id,
                        # Inicializa otros campos según sea necesario
                        'name': f"Madurez para {job.name} - {job.maturity_level_id.name}"
                    })
                    job.maturity_data_id = maturity
            else:
                job.maturity_data_id = False

    # _sql_constraints = [
    #     ('unique_job_level', 'unique(job_id, level_id)', 'Ya existe una madurez para este puesto y nivel de madurez.')
    # ]


class HrJobMarurity(models.Model):
    _inherit = 'hr.job'

    maturity_level_id = fields.Many2one(
        'hr.job.maturity.level', 
        string='Nivel de Madurez'
    )
    maturity_ids = fields.One2many(
        'hr.job.maturity', 
        'job_id', 
        string='Niveles de Madurez'
    )

    # Campo computado para obtener el registro de hr.job.maturity correspondiente
    maturity_data_id = fields.Many2one(
        'hr.job.maturity', 
        string="Datos de Madurez", 
        compute='_compute_maturity_data', 
        store=True
    )

    # Campos relacionados para mostrar los datos de hr.job.maturity
    graduation_time = fields.Char(
        related='maturity_data_id.graduation_time', 
        string="Tiempo de Graduación", 
        
    )

    currency_id = fields.Many2one(
        'res.currency', 
        string='Moneda', 
        required=True, 
        default=lambda self: self.env.company.currency_id
    )

    fixed_salary = fields.Monetary(
        related='maturity_data_id.fixed_salary', 
        string="Salario Fijo", 
        
    )
    variable_salary = fields.Float(
        related='maturity_data_id.variable_salary', 
        string="Salario Variable", 
        digits=(6, 2), 
        
    )
    full_salary = fields.Monetary(
        related='maturity_data_id.full_salary', 
        string="Salario Integral", 
        
    )
    vacancy_ratio = fields.Float(
        related='maturity_data_id.vacancy_ratio', 
        string="Ratio por Vacante", 
        
    )
    direct_staff = fields.Integer(
        related='maturity_data_id.direct_staff', 
        string="Personal Directo", 
        
    )
    indirect_staff = fields.Integer(
        related='maturity_data_id.indirect_staff', 
        string="Personal Indirecto", 
        
    )
    schooling_id = fields.Many2one(
        related='maturity_data_id.schooling_id', 
        string='Jefe Funcional', 
        
    )
    minimum_age = fields.Integer(
        related='maturity_data_id.minimum_age', 
        string="Edad Mínima", 
        
    )
    language = fields.Char(
        related='maturity_data_id.language', 
        string="Idioma", 
        
    )
    courses_ids = fields.Many2many(
        related='maturity_data_id.courses_ids', 
        string="Cursos", 
        
    )

    @api.depends('maturity_level_id', 'maturity_ids')
    def _compute_maturity_data(self):
        for job in self:
            if job.maturity_level_id:
                maturity = job.maturity_ids.filtered(lambda m: m.level_id == job.maturity_level_id)
                if maturity:
                    job.maturity_data_id = maturity[0]
                else:
                    # Opcional: Crear automáticamente el registro de madurez si no existe
                    maturity = self.env['hr.job.maturity'].create({
                        'job_id': job.id,
                        'level_id': job.maturity_level_id.id,
                        # Inicializa otros campos según sea necesario
                        'name': f"Madurez para {job.name} - {job.maturity_level_id.name}"
                    })
                    job.maturity_data_id = maturity
            else:
                job.maturity_data_id = False
