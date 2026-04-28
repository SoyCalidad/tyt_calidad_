from odoo import models, fields 
from odoo.exceptions import UserError

class RiskNotificationRevision(models.TransientModel):
    _name = "tyt.risk.notification.revision"
    _description = "Notificacion revision riesgo"

    risk_id = fields.Many2one(
        comodel_name='tyt.risk.management',
        string="Riesgo"
    )
    name = fields.Text("Comentario")

    def action_notify(self):
        self.ensure_one()
        if not self.name:
            raise UserError(
                "Debe escribir un mensaje",
            )

        self.env['tyt.risk.mo_comment'].create([{
            'risk_id': self.risk_id.id,
            'name': self.name,
        }])
        self.risk_id.write({
            'status': 'review',
        })

    #     return {
    #     'type': 'ir.actions.act_window_close'
    # }
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'OK',
                'message': 'Enviado para su revision',
                'type': 'success',
            }
        }