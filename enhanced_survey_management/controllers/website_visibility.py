# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Mohammed Savad, Ahammed Harshad (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0(OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the
#    Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
###############################################################################
from odoo import http
from odoo.http import request
from odoo import api, exceptions, fields, models, _


class WebsiteView(http.Controller):
    """Inherited http.Controller to add custom route"""

    @http.route('/my/surveys', type='http', auth="user", website=True)
    def portal_user_access(self):
        """ Controller function to access survey from website """

        current_date = fields.Date.context_today(http.request.env.user)
        surveys = request.env['survey.survey'].sudo().search(
            [('access_mode', '=', 'website'), ('is_published', '=', True), ('published_date', '<=', current_date)],
            order='published_date desc',
        )
        values = {
            'survey_list': [{
                'title': rec.title,
                'attempts': rec.attempts_limit,
                'date': rec.create_date,
                'published_date': rec.published_date,
                'access_token': rec.access_token
            } for rec in surveys],
            'page_name': 'survey',
        }
        return request.render("enhanced_survey_management.survey_visibility", values)