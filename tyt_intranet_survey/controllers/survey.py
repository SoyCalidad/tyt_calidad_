from odoo import http
from odoo.http import request
from odoo import api, exceptions, fields, models, _


class SurveyController(http.Controller):
    """Inherited http.Controller to add custom route"""

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
                'published_start_date': rec.published_start_date.strftime('%d/%m/%Y') if rec.published_start_date else '',
                'published_end_date': rec.published_end_date.strftime('%d/%m/%Y') if rec.published_end_date else '',
                'access_token': rec.access_token
            } for rec in surveys],
            'page_name': 'survey',
        }
        return request.render('tyt_intranet_survey.portal_my_surveys', values)
