"""Añadidos objetivos a contexto
"""

from odoo import models, fields


class Context(models.Model):
    """Reemplaza el campo goals por target_ids para tener coherencia
    con el sistema"""
    
    _inherit = 'mgmtsystem.context.policy'
    
    target_ids = fields.One2many('mgmtsystem.target', 'process_id', string='Objetivos')

class Target(models.Model):
    _inherit = 'mgmtsystem.target'
    
    context_policy_id = fields.Many2one('mgmtsystem.context.policy', string='Política')


class PESTFactor(models.Model):
    _inherit = 'pest.factor'

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')