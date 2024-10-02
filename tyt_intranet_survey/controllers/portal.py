from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import http
from odoo.http import request


class SurveyPortal(CustomerPortal):
    """ Inherited CustomerPortal to add new portal view"""

    def _prepare_home_portal_values(self, counters):
        """ Function : Prepare portal values for attended survey count
            @return : Survey counts
        """
        values = super(SurveyPortal, self)._prepare_home_portal_values(
            counters)
        if 'survey_count' in counters:
            values['survey_count'] = request.env[
                'survey.survey'].sudo().search_count([
                ('user_id', '=', request.uid)])
        return values
