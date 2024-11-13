from odoo import models, fields

class HrJob(models.Model):
    _inherit = 'hr.job'

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

    
    filosofia_organizacional = fields.Text(string="Filosofía Organizacional")
    relacion_interna = fields.Text(string="Relación Interna")
    relacion_externa = fields.Text(string="Relación Externa")
    valores = fields.Text(string="Valores")
    plan_estrategico = fields.Text(string="Plan Estratégico")
    
    puntos_valuacion = fields.Char(string="Puntos (Valuación)")
    categoria = fields.Char(string="Categoría")
    nivel_organizacional = fields.Char(string="Nivel Organizacional")
    


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'  
    
    first_option = fields.Many2one('hr.job', string='Primera Opción')
    second_option = fields.Many2one('hr.job', string='Segunda Opción')
    third_option = fields.Many2one('hr.job', string='Tercera Opción')
    curso = fields.Text(string="Curso (S)")
    
    tiempo_graduacion = fields.Char(string="Tiempo de Graduación", help="Tiempo estimado en meses o años")
    salario_fijo = fields.Float(string="Salario Fijo", help="Salario base del candidato")
    salario_variable = fields.Float(string="Salario Variable", help="Porcentaje de salario variable")
    salario_integral = fields.Float(string="Salario Integral", help="El salario total incluyendo salario fijo y variable")
    ratio_vacante = fields.Integer(string="Ratio p/ Vacante", help="Proporción de candidatos por vacante")
    personal_directo = fields.Char(string="Personal Directo", help="Número de personas en el área directa (rango)")
    personal_indirecto = fields.Char(string="Personal Indirecto", help="Número de personas en el área indirecta (rango)")
    escolaridad = fields.Char(string="Escolaridad", help="Nivel de escolaridad del candidato")
    edad_minima = fields.Integer(string="Edad Mínima", help="Edad mínima requerida para el puesto")
    idiomas = fields.Char(string="Idiomas", help="Idiomas hablados por el candidato")
    
