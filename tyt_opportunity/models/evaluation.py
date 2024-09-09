from odoo import models, api
from odoo.exceptions import UserError

class ModifiedResult(models.Model):
    _inherit = 'evaluation.result'

    @api.constrains('value')
    def _constrains_value(self):
        for each in self:
            if each.value < each.alternative.value_less or each.value > each.alternative.value_high:
                msg = 'El valor tiene que estar entre %s y %s' % (each.alternative.value_less, each.alternative.value_high)
                raise UserError(msg)
