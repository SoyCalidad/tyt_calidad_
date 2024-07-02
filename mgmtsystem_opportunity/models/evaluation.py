# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Result(models.Model):
    _name = 'evaluation.result'

    criterio_id = fields.Many2one(
        string='Criterio',
        comodel_name='evaluation.criterio',
        ondelete='restrict',
    )
    name = fields.Char(
        string='Nombre',
        related='criterio_id.name',
        store=True,
    )
    description = fields.Text(
        string='Descripción',
    )
    value = fields.Integer(
        string='Valor',
    )
    alternative = fields.Many2one(comodel_name='evaluation.criterio.line', string='Alternativa', domain="[('criterio_id','=',criterio_id)]")
    
    alternative_description = fields.Text(related='alternative.description', string='Descripción de la alternativa')
    
    text_values = fields.Char(compute='_compute_text_values', string='Valores')
    
    @api.depends('alternative')
    def _compute_text_values(self):
        text_values = ''
        alternative = self.alternative
        if alternative:
            text_values = 'El valor mínimo es %s y el máximo es %s' % (alternative.value_less, alternative.value_high)
        self.text_values = text_values

    @api.onchange('value')
    def _onchange_value(self):
        if self.value < self.alternative.value_less or self.value > self.alternative.value_high:
            msg = 'El valor tiene que estar entre %s y %s' % (self.alternative.value_less, self.alternative.value_high)
            raise UserError(msg)
    
    @api.constrains('value')
    def _constrains_value(self):
        for each in self:
            if each.value < each.alternative.value_less or each.value > each.alternative.value_high:
                msg = 'El valor tiene que estar entre %s y %s' % (each.alternative.value_less, each.alternative.value_high)
                raise UserError(msg)
            if each.value == 0:
                msg = 'El valor del resultado %s no puede ser 0' % each.criterio_id.name
                raise UserError(msg)


class Eval(models.Model):
    _name = 'evaluation.evaluation'

    name = fields.Char(
        string='Nombre',
        required=True,
    )

    type = fields.Selection(
        string='Tipo',
        selection=[
            ('risk', 'Riesgo'),
            ('opportunity', 'Oportunidad')],
    )
    criterio_ids = fields.One2many(
        string='Criterios',
        comodel_name='evaluation.criterio',
        inverse_name='evaluation_id',
    )
    active = fields.Boolean(
        string='Activo',
        default=True,
    )


class Criterio(models.Model):
    _name = 'evaluation.criterio'

    name = fields.Char(
        string='Nombre',
        required=True,
    )
    description = fields.Text(string='Descripción')
    evaluation_id = fields.Many2one(
        string='Evaluación',
        comodel_name='evaluation.evaluation',
        ondelete='restrict',
    )
    type = fields.Selection(
        string='Tipo',
        related='evaluation_id.type'
    )
    line_ids = fields.One2many(
        string='Alternativas',
        comodel_name='evaluation.criterio.line',
        inverse_name='criterio_id',
    )
   


class CriterioLine(models.Model):
    _name = 'evaluation.criterio.line'

    name = fields.Char(
        string='Nombre',
        required=True,
    )
    criterio_id = fields.Many2one(
        string='Criterio',
        comodel_name='evaluation.criterio',
        ondelete='restrict',
    )
    type = fields.Selection(
        string='Tipo',
        related='criterio_id.type',
    )
    description = fields.Text(
        string='Descripción',
    )
    value_less = fields.Integer(
        string='Valor menor',
    )
    value_high = fields.Integer(
        string='Valor mayor',
    )
