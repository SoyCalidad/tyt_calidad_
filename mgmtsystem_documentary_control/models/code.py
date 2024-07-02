from odoo import api, fields, models


class MgmtsystemCode(models.AbstractModel):
    _name = 'mgmtsystem.code'
    _description = 'Código de modelo'

    """Gestión de códigos para los modelos de Soy Calidad.
    Permite gestionar y automatizar los códigos de los modelos de la aplicación.
    """

    code = fields.Char('Código')
    old_code = fields.Char('Código antiguo')

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        dirs = res.__dir__()
        if 'code' in dirs:
            documentary_control_id = self.env['documentary.control'].search(
                [('model_id.model', '=', res._name)], limit=1)
            if documentary_control_id:
                res.code = documentary_control_id.code
        return res

    def write(self, vals):
        res = super().write(vals)
        dirs = res.__dir__()
        if 'code' in dirs:
            documentary_control_id = self.env['documentary.control'].search(
                [('model_id.model', '=', res._name)], limit=1)
            if documentary_control_id:
                res.code = documentary_control_id.code
        return res
