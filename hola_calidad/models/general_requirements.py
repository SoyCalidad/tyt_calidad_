from odoo import api, fields, models


class GeneralStandard(models.Model):
    _name = 'general.standard'
    _description = 'Norma'

    name = fields.Char('Nombre', required=True)


class GeneralRequirement(models.AbstractModel):
    _name = 'general.requirement'
    _description = 'General Requirement'

    name = fields.Char('Requerimiento', required=True)
    standard_id = fields.Many2one(
        'general.standard', string='Norma', required=True)


class RequirementIso9001(models.Model):
    _name = 'iso_9001.requirement'
    _inherit = 'general.requirement'
    _description = 'Requisito de norma ISO 9001'
