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


class SurveyController(http.Controller):
    """Inherited http.Controller to add custom route"""

    @api.model
    def format_date_spanish(self, date_obj):
        if not date_obj:
            return ''
        month_map = {
            '01': 'ene', '02': 'feb', '03': 'mar', '04': 'abr',
            '05': 'may', '06': 'jun', '07': 'jul', '08': 'ago',
            '09': 'sep', '10': 'oct', '11': 'nov', '12': 'dic'
        }
        return date_obj.strftime(f"%d {month_map[date_obj.strftime('%m')]} %Y")

    @http.route('/my/surveys', type='http', auth="user", website=True)
    def portal_my_survey(self):

        print('############################################')
        print('/my/surveys')
        print('############################################')

        partner = request.env.user.partner_id
        domain = [
            ('access_mode', '=', 'intranet'),
            ('is_published', '=', True),
            ('published_start_date', '<=', fields.Date.context_today(request.env.user)),
            ('published_end_date', '>=', fields.Date.context_today(request.env.user)),
            ('user_ids', 'in', [request.env.user.id])
        ]
        surveys = request.env['survey.survey'].sudo().search(domain, order='published_start_date desc')
        values = {
            'survey_list': [{
                'title': rec.title,
                'attempts': rec.attempts_limit,
                'date': rec.create_date,
                'published_start_date': self.format_date_spanish(rec.published_start_date) if rec.published_start_date else '',
                'published_end_date': self.format_date_spanish(rec.published_end_date) if rec.published_end_date else '',
                'access_token': rec.access_token,
                'has_answered': rec._has_survey_answered(partner),
                'answer_state': ANSWER_STATES.get(rec._get_survey_answer_state(partner)),
                'color_state': COLOR_STATES.get(rec._get_survey_answer_state(partner)),
            } for rec in surveys],
            'page_name': 'survey',
        }
        response = request.render('tyt_intranet_survey.portal_my_surveys', values)
        return response

    @http.route('/survey/start/<string:survey_token>', type='http', auth='public', website=True)
    def survey_start(self, survey_token, answer_token=None, email=False, **post):

        print('############################################')
        print('/survey/start')
        print('############################################')

        """ Start a survey by providing
         * a token linked to a survey;
         * a token linked to an answer or generate a new token if access is allowed;
        """
        # Get the current answer token from cookie
        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get('survey_%s' % survey_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(survey_token, answer_token, ensure_token=False)

        if answer_from_cookie and access_data['validity_code'] in ('answer_wrong_user', 'token_wrong'):
            # If the cookie had been generated for another user or does not correspond to any existing answer object
            # (probably because it has been deleted), ignore it and redo the check.
            # The cookie will be replaced by a legit value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(survey_token, None, ensure_token=False)

        if access_data['validity_code'] is not True:
            return self._redirect_with_error(access_data, access_data['validity_code'])

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data['answer_sudo']
        if not answer_sudo:
            try:
                answer_sudo = survey_sudo._create_answer(user=request.env.user, email=email)
            except UserError:
                answer_sudo = False

        if not answer_sudo:
            try:
                survey_sudo.with_user(request.env.user).check_access_rights('read')
                survey_sudo.with_user(request.env.user).check_access_rule('read')
            except:
                return request.redirect("/")
            else:
                return request.render("survey.survey_403_page", {'survey': survey_sudo})

        return request.redirect('/survey/%s/%s' % (survey_sudo.access_token, answer_sudo.access_token))
