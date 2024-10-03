from odoo import http
from odoo.http import request
from odoo import api, exceptions, fields, models, _
from datetime import datetime


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
        current_date = fields.Date.context_today(request.env.user)
        surveys = request.env['survey.survey'].sudo().search([
            ('access_mode', '=', 'intranet'),
            ('is_published', '=', True),
            ('published_start_date', '<=', current_date),
            ('published_end_date', '>=', current_date),
            ('user_ids', 'in', [request.env.user.id]),
        ], order='published_start_date desc')
        values = {
            'survey_list': [{
                'title': rec.title,
                'attempts': rec.attempts_limit,
                'date': rec.create_date,
                'published_start_date': self.format_date_spanish(rec.published_start_date) if rec.published_start_date else '',
                'published_end_date': self.format_date_spanish(rec.published_end_date) if rec.published_end_date else '',
                'access_token': rec.access_token
            } for rec in surveys],
            'page_name': 'survey',
        }
        return request.render('tyt_intranet_survey.portal_my_surveys', values)
