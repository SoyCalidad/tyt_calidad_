import uuid

from odoo import models, fields, api, _


class ProcessEdition(models.Model):
    _inherit = 'process.edition'

    access_token = fields.Char(string="Access Token", default=lambda self: str(uuid.uuid4()), readonly=True, copy=False)

    def send_edition_by_email(self):
        template = 'tyt_share.mail_template_process_edition'
        return self.notify_users_by_email(template)

    def get_share_url(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        share_url = f'{base_url}/edition/share/{self.id}/{self.access_token}'
        return share_url
