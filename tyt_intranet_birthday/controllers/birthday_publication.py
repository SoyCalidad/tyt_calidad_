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

from operator import itemgetter

from markupsafe import Markup

from odoo import http
from odoo.exceptions import AccessError, MissingError, UserError
from odoo.http import request
from odoo.tools.translate import _
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.osv.expression import OR, AND
from odoo.http import content_disposition, Controller, request, route

_logger = logging.getLogger(__name__)


class BirthdayPublicationPortal(portal.CustomerPortal):

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        print('################ /my', '/my/home ################')

        values = self._prepare_portal_layout_values()

        print('values', values)

        user = request.env.user
        print('user', user)
        show_birthday_card_modal = user.x_studio_empleado.is_birthday
        print('show_birthday_card_modal', show_birthday_card_modal)

        if request.session.get('birthday_card_modal_shown'):
            print('request.session.get(birthday_card_modal_shown)', request.session.get('birthday_card_modal_shown'))
            show_birthday_card_modal = False
        else:
            request.session['birthday_card_modal_shown'] = True
            print('request.session[birthday_card_modal_shown]', request.session['birthday_card_modal_shown'])

        print('[END] show_birthday_card_modal', show_birthday_card_modal)
        values.update({
            'show_birthday_card_modal': show_birthday_card_modal,
        })

        return request.render("tyt_intranet_birthday.portal_my_home", values)


    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        return values

    def _prepare_birthday_publication_domain(self):

        return []

    @http.route(['/birthday_publication', '/birthday_publication/page/<int:page>'], type='http', auth='user', website=True)
    def portal_birthday_publication(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='subject', **kw):
        values = self._prepare_birthday_publication_values(page, date_begin, date_end, sortby, filterby, search, groupby, search_in)
        return request.render('tyt_intranet_birthday.portal_birthday_publication', values)

    def _prepare_birthday_publication_values(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='subject'):

        values = self._prepare_portal_layout_values()
        domain = self._prepare_birthday_publication_domain()

        employees = request.env['hr.employee'].sudo().search([])

        values.update({
            'page_name': 'birthday_publication',
            'default_url': '/birthday_publication',
            'employees': employees,
        })
        return values
