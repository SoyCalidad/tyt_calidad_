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


class MailboxController(http.Controller):

    @http.route('/mailbox', type='http', auth='user', website=True)
    def mailbox_form(self):
        values = request.params.copy()
        site_ids = request.env['x_sitios'].sudo().search([])
        user_site = request.env.user.x_studio_sitio.x_studio_sitios
        values['user_site_id'] = user_site.id if user_site and user_site.id in site_ids.ids else None
        values['site_ids'] = site_ids
        values['service_area_ids'] = request.env['tyt.intranet.service_area'].sudo().search([])
        values['message_type_ids'] = request.env['tyt.intranet.message_type'].sudo().search([])
        return request.render('tyt_intranet_helpdesk.mailbox_form', values)

    @http.route(['/mailbox_send'], type='http', methods=['POST'], auth='user', website=True)
    def mailbox_form_send(self, **kw):
        Mailbox = request.env['tyt.intranet.mailbox']
        mailbox_values = {}

        if 'receive_response' in kw:
            mailbox_values['receive_response'] = True

        if 'is_anonymous' in kw:
            mailbox_values['is_anonymous'] = True
            mailbox_values['user_id'] = False
            mailbox_values['receive_response'] = False
        else:
            mailbox_values['is_anonymous'] = False
            mailbox_values['user_id'] = request.env.user.id

        for key, value in kw.items():
            if key in ['service_area_id', 'message_type_id']:
                mailbox_values[key] = int(value)
            if key in ['comment']:
                mailbox_values[key] = value

        if 'is_anonymous' in kw:
            mailbox_values['site_id'] = kw.get('site_id_select')
        else:
            mailbox_values['site_id'] = kw.get('site_id')

        mailbox = Mailbox.sudo().create(mailbox_values)
        mailbox.sudo().send_mail()
        return request.redirect('/mailbox/success')

    @http.route('/mailbox/success', type='http', auth='user', website=True)
    def mailbox_form_confirmation(self):
        return request.render('tyt_intranet_helpdesk.mailbox_form_send')

    @http.route(['/my/mailbox', '/my/mailbox/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_mailbox(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = {}
        mailbox_records = request.env['tyt.intranet.mailbox'].sudo().search([('user_id', '=', request.env.user.id)])
        values.update({
            'mailbox_records': mailbox_records,
        })
        return request.render('tyt_intranet_helpdesk.portal_my_mailbox', values)

    @http.route([
        '/my/mailbox/<int:entry_id>',
        '/my/mailbox/<int:entry_id>/<access_token>'
    ], type='http', auth="user", website=True)
    def mailbox_followup(self, entry_id=None, access_token=None, **kw):

        entry = request.env['tyt.intranet.mailbox'].sudo().browse(entry_id)
        values = {
            'entry': entry,
        }
        return request.render("tyt_intranet_helpdesk.mailbox_followup", values)
