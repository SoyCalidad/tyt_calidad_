from odoo import api, fields, models
from odoo.exceptions import ValidationError


class InternalIssue(models.Model):
    _inherit = 'mgmtsystem.context.internal_issue'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'internal_issue_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'internal_issue_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'internal_issue_validation_id', string='Validación')
    
    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class InternalIssueValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    internal_issue_elaboration_id = fields.Many2one(
        'mgmtsystem.context.internal_issue', string='Padre (Elaboración)')
    internal_issue_review_id = fields.Many2one(
        'mgmtsystem.context.internal_issue', string='Padre (Revisión)')
    internal_issue_validation_id = fields.Many2one(
        'mgmtsystem.context.internal_issue', string='Padre (Validación)')


class Policy(models.Model):
    _inherit = 'mgmtsystem.context.policy'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'policy_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'policy_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'policy_validation_id', string='Validación')
    
    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class PolicyValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    policy_elaboration_id = fields.Many2one(
        'mgmtsystem.context.policy', string='Padre (Elaboración)')
    policy_review_id = fields.Many2one(
        'mgmtsystem.context.policy', string='Padre (Revisión)')
    policy_validation_id = fields.Many2one(
        'mgmtsystem.context.policy', string='Padre (Validación)')


class ExternalIssue(models.Model):
    _inherit = 'mgmtsystem.context.external_issue'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'external_issue_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'external_issue_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'external_issue_validation_id', string='Validación')
    
    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class ExternalIssueValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    external_issue_elaboration_id = fields.Many2one(
        'mgmtsystem.context.external_issue', string='Padre (Elaboración)')
    external_issue_review_id = fields.Many2one(
        'mgmtsystem.context.external_issue', string='Padre (Revisión)')
    external_issue_validation_id = fields.Many2one(
        'mgmtsystem.context.external_issue', string='Padre (Validación)')
    
    


class Stakeholders(models.Model):
    _inherit = 'mgmtsystem.stakeholders'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'stakeholders_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'stakeholders_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'stakeholders_validation_id', string='Validación')
    
    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class StakeholdersValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    stakeholders_elaboration_id = fields.Many2one(
        'mgmtsystem.stakeholders', string='Padre (Elaboración)')
    stakeholders_review_id = fields.Many2one(
        'mgmtsystem.stakeholders', string='Padre (Revisión)')
    stakeholders_validation_id = fields.Many2one(
        'mgmtsystem.stakeholders', string='Padre (Validación)')


class OrganizationChart(models.Model):
    _inherit = 'mgmtsystem.context.organization_chart'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'organization_chart_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'organization_chart_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'organization_chart_validation_id', string='Validación')
    
    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class OrganizationChartValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    organization_chart_elaboration_id = fields.Many2one(
        'mgmtsystem.context.organization_chart', string='Padre (Elaboración)')
    organization_chart_review_id = fields.Many2one(
        'mgmtsystem.context.organization_chart', string='Padre (Revisión)')
    organization_chart_validation_id = fields.Many2one(
        'mgmtsystem.context.organization_chart', string='Padre (Validación)')

class PEST(models.Model):
    _inherit = 'mgmtsystem.context.pest'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'pest_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'pest_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'pest_validation_id', string='Validación')
    
    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class PESTValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    pest_elaboration_id = fields.Many2one(
        'mgmtsystem.context.pest', string='Padre (Elaboración)')
    pest_review_id = fields.Many2one(
        'mgmtsystem.context.pest', string='Padre (Revisión)')
    pest_validation_id = fields.Many2one(
        'mgmtsystem.context.pest', string='Padre (Validación)')

class SWOT(models.Model):
    _inherit = 'mgmtsystem.context.swot'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'swot_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'swot_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'swot_validation_id', string='Validación')
    
    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class SWOTValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    swot_elaboration_id = fields.Many2one(
        'mgmtsystem.context.swot', string='Padre (Elaboración)')
    swot_review_id = fields.Many2one(
        'mgmtsystem.context.swot', string='Padre (Revisión)')
    swot_validation_id = fields.Many2one(
        'mgmtsystem.context.swot', string='Padre (Validación)')

class CrossSWOT(models.Model):
    _inherit = 'mgmtsystem.context.cross.swot'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'cross_swot_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'cross_swot_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'cross_swot_validation_id', string='Validación')
    
    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class CrossSWOTValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    cross_swot_elaboration_id = fields.Many2one(
        'mgmtsystem.context.cross.swot', string='Padre (Elaboración)')
    cross_swot_review_id = fields.Many2one(
        'mgmtsystem.context.cross.swot', string='Padre (Revisión)')
    cross_swot_validation_id = fields.Many2one(
        'mgmtsystem.context.cross.swot', string='Padre (Validación)')
