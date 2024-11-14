from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrJobMarurityLevel(models.Model):
    _name = 'hr.job.maturity.level'
    _description = "Niveles de Madurez"
    
    name = fields.Char()
    
class HrJobMaruritySchooling(models.Model):
    _name = 'hr.job.maturity.schooling'
    _description = "Madurez / Escolaridad"
    name = fields.Char(string="Nombre")
    
class HrJobMarurityCourses(models.Model):
    _name = 'hr.job.maturity.courses'
    _description = "Madurez / Cursos"
    name = fields.Char(string="Nombre")
    
class HrJobMarurity(models.Model):
    _name = 'hr.job.maturity'
    _description = 'Detalles por Nivel'
    
    job_id = fields.Many2one('hr.job', string='Puesto')
    nivel_id = fields.Many2one('hr.job.maturity.level', string='Nivel de Madurez')
    tiempo_graduacion = fields.Char(string="Tiempo de Graduación", help="Tiempo estimado en meses o años")
    
    currency_id = fields.Many2one(
        'res.currency', 
        string='Moneda', 
        required=True, 
        default=lambda self: self.env.company.currency_id
    )
    
    salario_fijo = fields.Monetary(
        string="Salario Fijo",
        currency_field='currency_id'
    )
    salario_variable = fields.Float(string="Salario Variable", digits=(6, 2))
    salario_integral = fields.Monetary(
        string="Salario Integral",
        compute='_compute_salario_integral',
        store=True,
        currency_field='currency_id'
    )
    ratio_vacante = fields.Integer(string="Ratio p/ Vacante", help="Proporción de candidatos por vacante")
    personal_directo = fields.Char(string="Personal Directo", help="Número de personas en el área directa (rango)")
    personal_indirecto = fields.Char(string="Personal Indirecto", help="Número de personas en el área indirecta (rango)")
    
    escolaridad_id = fields.Many2one('hr.job.maturity.schooling', string='Jefe funcional')
    
    edad_minima = fields.Integer(string="Edad Mínima", help="Edad mínima requerida para el puesto")
    idiomas = fields.Char(string="Idiomas", help="Idiomas hablados por el candidato")
    
    curso_id = fields.Many2many(comodel_name='hr.job.maturity.courses', string="Cursos")
    
    
    sequence = fields.Integer(string="Secuencia")
    parent_id = fields.Many2one('hr.job', string="Relacionado con el registro principal")

    @api.constrains('parent_id', 'nivel')
    def _check_max_levels(self):
        for record in self:
            # Verificar que no haya más de 4 niveles
            if len(record.parent_id.nivel_detalle_ids) > 4:
                raise ValidationError("No puedes tener más de 4 niveles relacionados.")
            
            # Validar que no haya niveles duplicados para el mismo parent_id
            niveles = [detalle.nivel_id for detalle in record.parent_id.nivel_detalle_ids]
            if niveles.count(record.nivel_id) > 1:
                raise ValidationError(f"El nivel {record.nivel_id.name} ya está registrado para este trabajo.")
    
    @api.depends('salario_fijo', 'salario_variable')
    def _compute_salario_integral(self):
        for record in self:
            if record.salario_fijo and record.salario_variable:
                # Suponiendo que salario_variable es un decimal (ej. 0.05 para 5%)
                record.salario_integral = record.salario_fijo + (record.salario_fijo * record.salario_variable)
                
                # Si salario_variable es un entero representando el porcentaje (ej. 5 para 5%)
                # Descomenta la siguiente línea y comenta la anterior
                # record.salario_integral = record.salario_fijo + (record.salario_fijo * (record.salario_variable / 100))
            elif record.salario_fijo:
                record.salario_integral = record.salario_fijo
            else:
                record.salario_integral = 0.0
    @api.constrains('salario_fijo')
    def _check_salaries_positive(self):
        for record in self:
            if record.salario_fijo < 0:
                raise ValidationError("El Salario Fijo no puede ser negativo.")
            
    @api.constrains('salario_variable')
    def _check_salario_variable(self):
        for record in self:
            # Si salario_variable es un decimal
            if not (0.0 <= record.salario_variable <= 1.0):
                raise ValidationError("El Salario Variable debe estar entre 0% y 100% (0.0 a 1.0).")
            
            
class HrJob(models.Model):
    _inherit = 'hr.job'

    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    fondo_ahorro = fields.Text(string='Fondo de ahorro')
    beca_estudiantil = fields.Text(string='Beca estudiantil')
    r_casa = fields.Text(string='R. Casa')
    v_despensa = fields.Text(string='V. de despensa')
    v_gasolina = fields.Text(string='V. de gasolina')
    seguro_medico_mayor = fields.Text(string='Seguro de gastos médicos mayores')
    auto = fields.Text(string='Auto')

    objetivo_general = fields.Text(string='Objetivo General')
    objetivo_puesto = fields.Text(string='Objetivo del Puesto')
    
    finanzas_indicador = fields.Char(string="Indicador Finanzas")
    finanzas_meta = fields.Float(string="Meta Finanzas (%)")

    cliente_indicador = fields.Char(string="Indicador Cliente")
    cliente_meta = fields.Float(string="Meta Cliente (%)")

    procesos_indicador = fields.Char(string="Indicador Procesos")
    procesos_meta = fields.Float(string="Meta Procesos (%)")

    gente_indicador = fields.Char(string="Indicador Gente")
    gente_meta = fields.Float(string="Meta Gente (%)")

    estrategico_indicador = fields.Char(string="Indicador Estratégico")
    estrategico_meta = fields.Float(string="Meta Estratégico (%)")

    costo_indicador = fields.Char(string="Indicador Costo")
    costo_meta = fields.Float(string="Meta Costo (%)")

    velocidad_respuesta_indicador = fields.Char(string="Indicador Velocidad de Respuesta")
    velocidad_respuesta_meta = fields.Float(string="Meta Velocidad de Respuesta (%)")

    disponibilidad_indicador = fields.Char(string="Indicador Disponibilidad")
    disponibilidad_meta = fields.Float(string="Meta Disponibilidad (%)")

    efectividad_proceso_indicador = fields.Char(string="Indicador Efectividad de Proceso")
    efectividad_proceso_meta = fields.Float(string="Meta Efectividad de Proceso (%)")

    
    
    relacion_interna = fields.Text(string="Relación Interna")
    relacion_externa = fields.Text(string="Relación Externa")
    valores = fields.Text(string="Valores")
    plan_estrategico = fields.Text(string="Plan Estratégico")
    
    nombre_corto = fields.Char(string="Nombre Corto")
    puntos_valuacion = fields.Char(string="Puntos (Valuación)")
    categoria = fields.Char(string="Categoría")
    nivel_organizacional = fields.Char(string="Nivel Organizacional")
    
    first_option = fields.Many2one('hr.job', string='Primera Opción')
    second_option = fields.Many2one('hr.job', string='Segunda Opción')
    third_option = fields.Many2one('hr.job', string='Tercera Opción')
    
    nivel_detalle_ids = fields.One2many(
        'hr.job.maturity', 
        'job_id', 
        string='Niveles de Madurez'
    )