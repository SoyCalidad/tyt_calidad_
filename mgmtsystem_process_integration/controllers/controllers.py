# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.addons.web.controllers.main import Home, ensure_db, redirect_with_hash
from odoo.http import request


class AvoidDebug(Home, http.Controller):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        ensure_db()
        if 'debug' in kw.keys():
            return redirect_with_hash('/web')
        return super(AvoidDebug, self).web_client(s_action=s_action, **kw)


