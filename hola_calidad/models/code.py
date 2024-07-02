from odoo import api, fields, models


class MgmtsystemCode(models.Model):
    _name = 'mgmtsystem.code'
    _description = 'Código de modelo'

    """Gestión de códigos para los modelos de Soy Calidad.
    Permite gestionar y automatizar los códigos de los modelos de la aplicación.
    """

    name = fields.Char('Nombre')
    model_name = fields.Char('Nombre del modelo')
    sequence_id = fields.Many2one('ir.sequence', string='Entry Sequence',
                                  help="Permite añadir y personalizar la secuencia.", required=True, copy=False)
