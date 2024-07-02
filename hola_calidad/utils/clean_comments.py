from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.http import request

"""Clean message_ids allowing only 1 month of messages"""

class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def _cron_clean_message_ids(self):
        """Clean message_ids allowing only 1 month of messages"""
        date_limit = fields.Datetime.to_string(
            fields.Datetime.from_string(fields.Datetime.now()) -
            fields.Date._get_timedelta(days=30))
        self.search([('date', '<', date_limit)]).unlink()

