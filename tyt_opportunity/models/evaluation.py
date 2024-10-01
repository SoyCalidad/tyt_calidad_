from odoo import models, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ModifiedResult(models.Model):
    _inherit = 'evaluation.result'

    @api.depends('alternative')
    def _compute_text_values(self):
        for record in self:
            if record.alternative:
                record.text_values = 'El valor mínimo es %s y el máximo es %s' % (
                    record.alternative.value_less, record.alternative.value_high)
            else:
                record.text_values = ''

    @api.onchange('alternative')
    def onchange_alternative(self):
        if self.alternative:
            # Asignar el valor mínimo al campo 'value'
            self.value = self.alternative.value_less

    @api.constrains('value')
    def _constrains_value(self):
        for each in self:
            if each.value < each.alternative.value_less or each.value > each.alternative.value_high:
                msg = 'El valor tiene que estar entre %s y %s' % (each.alternative.value_less, each.alternative.value_high)
                raise UserError(msg)

    '''
    @api.constrains('alternative', 'value')
    def constrains_alternative_value(self):
        for record in self:
            if record.alternative:
                if record.value < record.alternative.value_less or record.value > record.alternative.value_high:
                    msg = 'El valor (%s) debe estar entre %s y %s para la alternativa "%s".' % (
                        record.value, record.alternative.value_less, record.alternative.value_high, record.alternative.name)
                    raise UserError(msg)
    '''

    '''
    @api.onchange('alternative')
    def onchange_alternative(self):
        if self.alternative:
            if self.value:
                if self.value < self.alternative.value_less or self.value > self.alternative.value_high:
                    msg = 'El valor actual (%s) no está dentro del rango permitido (%s min - %s max) para la alternativa "%s". Por favor, ajuste el valor antes de continuar.' % (
                        self.value, self.alternative.value_less, self.alternative.value_high, self.alternative.name)
                    raise UserError(msg)
    '''