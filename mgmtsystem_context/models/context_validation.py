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
        'mgmtsystem.context.internal_issue')
    internal_issue_review_id = fields.Many2one(
        'mgmtsystem.context.internal_issue')
    internal_issue_validation_id = fields.Many2one(
        'mgmtsystem.context.internal_issue')


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
        'mgmtsystem.context.policy')
    policy_review_id = fields.Many2one(
        'mgmtsystem.context.policy')
    policy_validation_id = fields.Many2one(
        'mgmtsystem.context.policy')


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
        'mgmtsystem.context.external_issue')
    external_issue_review_id = fields.Many2one(
        'mgmtsystem.context.external_issue')
    external_issue_validation_id = fields.Many2one(
        'mgmtsystem.context.external_issue')
    
    


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
        'mgmtsystem.stakeholders')
    stakeholders_review_id = fields.Many2one(
        'mgmtsystem.stakeholders')
    stakeholders_validation_id = fields.Many2one(
        'mgmtsystem.stakeholders')


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
        'mgmtsystem.context.organization_chart')
    organization_chart_review_id = fields.Many2one(
        'mgmtsystem.context.organization_chart')
    organization_chart_validation_id = fields.Many2one(
        'mgmtsystem.context.organization_chart')

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
        'mgmtsystem.context.pest')
    pest_review_id = fields.Many2one(
        'mgmtsystem.context.pest')
    pest_validation_id = fields.Many2one(
        'mgmtsystem.context.pest')

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
        'mgmtsystem.context.swot')
    swot_review_id = fields.Many2one(
        'mgmtsystem.context.swot')
    swot_validation_id = fields.Many2one(
        'mgmtsystem.context.swot')

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
        'mgmtsystem.context.cross.swot')
    cross_swot_review_id = fields.Many2one(
        'mgmtsystem.context.cross.swot')
    cross_swot_validation_id = fields.Many2one(
        'mgmtsystem.context.cross.swot')
