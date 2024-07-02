from odoo import _, api, fields, models
from datetime import datetime


class PEST(models.Model):
    """PEST analysis (political, economic, socio-cultural and technological) describes a framework of macro-environmental factors used 
    in the environmental scanning component of strategic management. It is part of an external analysis when conducting a strategic
    analysis or doing market research, and gives an overview of the different macro-environmental factors to be taken into 
    consideration. It is a strategic tool for understanding market growth or decline, business position, potential and direction
    for operations.
    """
    _name = 'mgmtsystem.context.pest'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Análisis PESTEL'

    process_id = fields.Many2one(
        'mgmt.process', string='Proceso', domain=[('active','=',True)])

    custom_analysis = fields.Boolean(string='Análisis personalizado')

    politic_factor_ids = fields.Many2many(
        string='Factores políticos',
        comodel_name='pest.factor',
        relation='politic_pest_rel',
        domain=[('type_id_name', '=', 'Políticos')])
    economic_factor_ids = fields.Many2many(
        string='Factores económicos',
        comodel_name='pest.factor',
        relation='economic_pest_rel',
        domain=[('type_id_name', '=', 'Económicos')])
    sociocult_factor_ids = fields.Many2many(
        string='Factores socioculturales',
        comodel_name='pest.factor',
        relation='soccult_pest_rel',
        domain=[('type_id_name', '=', 'Socioculturales')])
    tech_factor_ids = fields.Many2many(
        string='Factores tecnológicos',
        comodel_name='pest.factor',
        relation='tech_pest_rel',
        domain=[('type_id_name', '=', 'Tecnológicos')])
    ecologic_factor_ids = fields.Many2many(
        string='Factores ecológicos',
        comodel_name='pest.factor',
        relation='ecologic_pest_rel',
        domain=[('type_id_name', '=', 'Ecológicos')])
    legal_factor_ids = fields.Many2many(
        string='Factores legales',
        comodel_name='pest.factor',
        relation='legal_pest_rel',
        domain=[('type_id_name', '=', 'Legales')])

    admin_factor_ids = fields.Many2many(
        string='Administración',
        comodel_name='pest.factor',
        relation='admin_amofhit_rel',
        domain=[('type_id_name', '=', 'Administración')])

    marketing_factor_ids = fields.Many2many(
        string='Marketing y ventas',
        comodel_name='pest.factor',
        relation='marketing_amofhit_rel',
        domain=[('type_id_name', '=', 'Marketing y ventas')])

    logistic_factor_ids = fields.Many2many(
        string='Operaciones, productos y logística',
        comodel_name='pest.factor',
        relation='logistic_amofhit_rel',
        domain=[('type_id_name', '=', 'Operaciones, productos y logística')])

    accounting_factor_ids = fields.Many2many(
        string='Finanzas y contabilidad',
        comodel_name='pest.factor',
        relation='accounting_amofhit_rel',
        domain=[('type_id_name', '=', 'Finanzas y contabilidad')])

    rrhh_factor_ids = fields.Many2many(
        string='Recursos humanos',
        comodel_name='pest.factor',
        relation='rrhh_amofhit_rel',
        domain=[('type_id_name', '=', 'Recursos humanos')])

    it_factor_ids = fields.Many2many(
        string='Sistemas de información y comunicaciones',
        comodel_name='pest.factor',
        relation='it_amofhit_rel',
        domain=[('type_id_name', '=', 'Sistemas de información y comunicaciones')])

    internal_tech_factor_ids = fields.Many2many(
        string='Tecnología, investigación y desarrollo',
        comodel_name='pest.factor',
        relation='internaltech_amofhit_rel',
        domain=[('type_id_name', '=', 'Tecnología, investigación y desarrollo')])

    name = fields.Char(string='Nombre del análisis')
    active = fields.Boolean('Active', default=True)

    analysis_date = fields.Datetime(string='Fecha de análisis')

    description = fields.Text(string='Comentarios')
    external_factor_ids = fields.Many2many(
        string='Factores externos (PESTEL)', comodel_name='pest.factor',
        relation='external_pest_rel', order='type desc', domain=[('type_id_type', '=', 'external')])
    internal_factor_ids = fields.Many2many(
        string='Factores internos (AMOFHIT)', comodel_name='pest.factor',
        relation='internal_pest_rel', order='type desc', domain=[('type_id_type', '=', 'internal')])

    factor_ids = fields.Many2many(
        string='Factores internos (AMOFHIT)', comodel_name='pest.factor',
        relation='factor_pest_rel', order='type desc', domain=[('type_id_type', '=', 'internal')])

    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.context.pest', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.context.pest', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_context.context_pest_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class PESTFactor(models.Model):
    _name = 'pest.factor'
    _description = 'Factor PESTEL'

    name = fields.Char(string='Nombre', required=False)
    type_id = fields.Many2one('pest.factor.type', string='Tipo', required=True)

    type_id_name = fields.Char(
        related='type_id.name', string='Tipo', store=True)
    type_id_type = fields.Selection(
        related='type_id.type', string='Tipo', store=True
    )
    details = fields.Text(string='Detalle')
    term = fields.Selection([
        ('short', 'Corto plazo'),
        ('medium', 'Mediano plazo'),
        ('large', 'Largo plazo'),
    ], string='Plazo')
    calification = fields.Selection([
        ('v_negative', 'Muy negativo'),
        ('negative', 'Negativo'),
        ('indifferent', 'Indiferente'),
        ('positive', 'Positivo'),
        ('v_positive', 'Muy positivo'),
    ], string='Impacto', required=True)
    risk_ids = fields.Many2many(
        'matrix.block.line', string='Riesgos', domain="[('type','=','risk')]", relation='ris_pesfactor_rel',
    )
    opportunity_ids = fields.Many2many(
        'matrix.block.line', string='Oportunidades', domain="[('type','=','opportunity')]", relation='op_pesfactor_rel',
    )


class FactorType(models.Model):
    _name = 'pest.factor.type'
    _description = 'Tipo de factor PESTEL'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    type = fields.Selection([
        ('external', 'PESTEL'),
        ('internal', 'AMOFHIT')
    ], string='Tipo')
