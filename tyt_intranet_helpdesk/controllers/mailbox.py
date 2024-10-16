from odoo import http
from odoo.http import request
from odoo import api, exceptions, fields, models, _
from datetime import datetime

import json
import logging
import werkzeug

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.http import request, content_disposition
from odoo.osv import expression
from odoo.tools import format_datetime, format_date, is_html_empty
from odoo.addons.base.models.ir_qweb import keep_query

_logger = logging.getLogger(__name__)


ANSWER_STATES = {
    'new': 'Todavía no empieza',
    'in_progress': 'En progreso',
    'done': 'Completado',
}

COLOR_STATES = {
    'new': 'info',
    'in_progress': 'warning',
    'done': 'success',
}


class MailboxController(http.Controller):

    @http.route('/mailbox', type='http', auth='public', website=True)
    def mailbox_form(self):


        values = request.params.copy()
        values['site_ids'] = request.env['x_sitios'].sudo().search([])
        values['service_area_ids'] = request.env['tyt.intranet.service_area'].sudo().search([])
        values['message_type_ids'] = request.env['tyt.intranet.message_type'].sudo().search([])

        values['name'] = request.env['tyt.intranet.message_type'].sudo().search([])

        return request.render('tyt_intranet_helpdesk.mailbox_form', values)

    @http.route(['/mailbox_send'], type='http', methods=['POST'], auth='public', website=True)
    def mailbox_form_send(self, **kw):
        Mailbox = request.env['tyt.intranet.mailbox']
        mailbox_values = {}

        for key, value in kw.items():
            if key in ['site_id', 'service_area_id', 'message_type_id']:
                mailbox_values[key] = int(value)
            if key in ['name', 'email', 'comment']:
                mailbox_values[key] = value

        if 'is_anonymous' in kw:
            mailbox_values['is_anonymous'] = True
        else:
            mailbox_values['is_anonymous'] = False

        mailbox = Mailbox.sudo().create(mailbox_values)
        return request.render('tyt_intranet_helpdesk.mailbox_form_send', {})
