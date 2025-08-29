# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.addons.web.controllers.webclient import WebClient
from odoo.http import request



class AvoidDebug(WebClient, http.Controller):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        if 'debug' in kw.keys():
            kw.pop('debug')
        return self.web_client(s_action=s_action, **kw)


