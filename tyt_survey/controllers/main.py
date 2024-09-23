# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import werkzeug
import base64
from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.http import request
import datetime

_logger = logging.getLogger(__name__)


class Complaint(http.Controller):

    @http.route('/satisfaction_survey_main', type='http', auth='public', website=True, sitemap=False)
    def satisfaction_survey_main(self, *args, **kw):
        values = request.params.copy()
        response = request.render('tyt_survey.satisfaction_survey_main', values)
        return response
