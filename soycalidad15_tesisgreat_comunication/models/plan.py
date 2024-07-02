from odoo import models, fields

class PlanLine(models.Model):
    _inherit = 'comunication.plan.line'

    date_release = fields.Char(
        string='Cuándo',
    )
    # El cliente Desea que el campo "Cuándo" sea "string" y no "datetime" o "date"
    # Sobreescribe el método _onchange_action_id para que no haga nada
    def _onchange_action_id(self):
        pass