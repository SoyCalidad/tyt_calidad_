from odoo import fields
from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.http import request

ANSWER_STATES = {
    'new': 'Todavía no empieza',
    'in_progress': 'En progreso',
    'done': 'Completado',
}

ANSWER_COLOR_STATES = {
    'new': 'info',
    'in_progress': 'warning',
    'done': 'success',
}


class SurveyPortal(portal.CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        return values

    def _prepare_survey_domain(self):
        user_groups = request.env.user.groups_id
        return [
            ('access_mode', '=', 'intranet'),
            ('publish_state', '=', 'published'),
            ('published_start_date', '<=', fields.Date.context_today(request.env.user)),
            ('published_end_date', '>=', fields.Date.context_today(request.env.user)),
            ('group_ids', 'in', user_groups.ids),
        ]

    @http.route('/my/surveys', type='http', auth='user', website=True)
    def portal_my_survey(self):
        values = self._prepare_portal_layout_values()
        domain = self._prepare_survey_domain()
        surveys = request.env['survey.survey'].sudo().search(domain, order='published_start_date desc')
        survey_data = []
        for survey in surveys:
            user_input = request.env['survey.user_input'].sudo().search([
                ('survey_id', '=', survey.id),
                ('partner_id', '=', request.env.user.partner_id.id)
            ], limit=1)
            survey_data.append({
                'survey': survey,
                'answer_token': user_input.access_token if user_input else None,
                'answer_state': ANSWER_STATES[user_input.state] if user_input else None,
                'answer_color_state': ANSWER_COLOR_STATES[user_input.state] if user_input else None,
            })
        values.update({
            'page_name': 'survey',
            'default_url': '/my/surveys',
            'survey_data': survey_data,
        })
        response = request.render('tyt_intranet_survey.portal_my_surveys', values)
        return response
