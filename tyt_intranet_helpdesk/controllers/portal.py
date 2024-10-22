from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import http
from odoo.http import request


class MailboxPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'mailbox_entry_count' in counters:
            values['mailbox_entry_count'] = request.env[
                'tyt.intranet.mailbox'].sudo().search_count([
                ('user_id', '=', request.uid)])
        return values
