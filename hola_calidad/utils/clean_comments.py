from odoo import api, fields, models

from datetime import timedelta

"""Clean message_ids allowing only 1 month of messages"""

class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def _cron_clean_message_ids(self):
        """Clean message_ids allowing only 1 month of messages"""
        date_limit = fields.Datetime.now() - timedelta(days=30)
        self.search([('date', '<', date_limit)]).unlink()

