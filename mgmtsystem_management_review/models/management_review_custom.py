from odoo import api, fields, models, _

class ManagementReview(models.Model):
    _inherit = 'management.review'

    # C.3

    policy_ids = fields.Many2many('mgmtsystem.context.policy', string='Poñiticas')
    policy_interpretation = fields.Text('Interpretación de políticas')
    
    # D.2. DESEMPEÑO DE LOS PROCESOS

    # process_perfomance = fields.Html('Process Perfomance')
    # process_perfomance_interpretation = fields.Html('Process Perfomance Interpretation')

    # D4. NO CONFORMIDADES Y ACCIONES CORRECTIVAS

    # nonconformity_and_action_ids = fields.Many2many('mgmtsystem.nonconformity', string='Nonconformities and Actions')
    # nonconformity_and_action_interpretation = fields.Html('Nonconformities and Actions Interpretation')

    # D5. LOS RESULTADOS DE SEGUIMIENTO Y MEDICIÓN

    # D6. RESULTADOS DE AUDITORÍAS

    # D7. DESEMPEÑO DE PROVEEDORES

    # E. ADECUACIÓN DE RECURSOS

    # F. EFICACIA DE ACCIONES PARA ABORDAR RIESGOS Y OPORTUNIDADES

    # H. LAS OPORTUNIDADES DE MEJORA CONTINUA




    