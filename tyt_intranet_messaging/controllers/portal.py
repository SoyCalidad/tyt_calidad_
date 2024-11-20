from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import http
from odoo.http import request
from odoo import fields


class DepartmentMessagePortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'department_message_entry_count' in counters:
            values['department_message_entry_count'] = request.env[
                'tyt.intranet.department_message'].sudo().search_count([
                ('user_id', '=', request.uid)])



        values['today_published_department_message_count'] = request.env['tyt.intranet.department_message'].sudo().search_count([
            ('state', '=', 'published'),
            ('published_date', '=', fields.Date.today()),
        ])
        print('#################')
        print('today_published_department_message_count', values['today_published_department_message_count'])

        return values
