from odoo import models, fields 
from odoo.exceptions import UserError

class RiskNotificationRevision(models.TransientModel):
    _name = "tyt.risk.notification.revision"
    _description = "Notificacion revision riesgo"

    risk_id = fields.Many2one(
        comodel_name='tyt.risk.management',
        string="Riesgo"
    ) #should be delete
    mitigation_id = fields.Many2one(
        comodel_name='tyt.risk.mitigation',
        string="Mitigación"
    )
    name = fields.Text("Comentario")

    def _send_notification_email(self, mitigation):
        # Datos para el correo
        current_user = self.env.user.display_name
        reviewer_email = mitigation.risk_id_reviewer_id.email 
        status_label = dict(mitigation._fields['status'].selection).get(mitigation.status, mitigation.status)
        
        if not reviewer_email:
            return # O lanza un ValidationError si es obligatorio

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # Formateo del cuerpo en HTML (Tabla invertida)
        body_html = f"""
            <h3>Actividad asignada</h3>
            <table border="1" class="table" style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left;">Actividad</th>
                    <td style="padding: 8px;">Monitoreo</td>
                </tr>
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left;">Descripción</th>
                    <td style="padding: 8px;">Monitoreo R{mitigation.risk_id_id} - {mitigation.risk_id_domain_id.display_name or ''}</td>
                </tr>
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left;">Estatus</th>
                    <td style="padding: 8px;">No Mitigado</td>
                </tr>
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left; width: 30%;">De</th>
                    <td style="padding: 8px;">{current_user}</td>
                </tr>
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left;">Comentario</th>
                    <td style="padding: 8px;">{self.name}</td>
                </tr>
            </table>
            <p>Estimado usuario, por favor revise sus actividades pendientes en la plataforma.</p>
            <div class="row justify-content-center">
            <a href="{base_url}" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" style="text-decoration: none; display: inline-block; color: rgb(255, 255, 255) !important; background-color: rgb(93, 71, 161) !important; border-radius: 4px; width: auto; border-width: 1px; border-style: solid; border-color: rgb(15, 11, 91); padding-top: 0px; padding-bottom: 5px; font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; text-align: center; word-break: keep-all;" data-linkindex="0" title="{base_url}" data-ogsb="rgb(15, 11, 91)"><span style="padding-left:20px; padding-right:20px; font-size:24px; display:inline-block; letter-spacing:normal"><span style="font-size:16px; margin:0px; line-height:2; word-break:break-word"><strong><span style="font-size:24px; line-height:48px">ODOO TYT</span></strong></span></span></a> 
            
            </div>
        """

        email_from = self.env.user.email_formatted or self.env.company.email_formatted
        if email_from:
            mail_values = {
                'subject': f'Mitigación R-{mitigation.risk_id_id}',
                'body_html': body_html,
                'email_to': reviewer_email,
                'email_from': email_from,
            }
            
            self.env['mail.mail'].sudo().create(mail_values).send()

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
        mitigation = self.mitigation_id
        
        
        mitigation.message_post(
            body=f"<b>Notificación enviada al revisor:</b><br/>",
            message_type='comment',
            subtype_xmlid='mail.mt_note',
            body_is_html=True,
        )
        self._send_notification_email(mitigation)

        mitigation.write({
            'status': 'under_review',
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
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }