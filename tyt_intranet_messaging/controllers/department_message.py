import logging
from operator import itemgetter

from odoo import fields
from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request
from odoo.osv.expression import OR, AND
from odoo.tools import groupby as groupbyelem
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class DepartmentMessagePortal(portal.CustomerPortal):

    def _prepare_department_messages_count_domain(self):
        user_groups = request.env.user.groups_id.ids
        return [
            ('published_date', '=', fields.Date.today()),
            ('state', '=', 'published'),
            ('group_ids', 'in', user_groups),
        ]
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        domain = self._prepare_department_messages_count_domain()
        if 'department_message_count' in counters:
            values['department_message_count'] = request.env['tyt.intranet.department_message'].sudo().search_count(domain)
        return values

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        return values

    def _prepare_department_messages_domain(self):
        user_groups = request.env.user.groups_id.ids
        return [
            '|',
            ('deadline_date', '=', False),
            ('deadline_date', '>=', fields.Date.today()),
            ('state', '=', 'published'),
            ('group_ids', 'in', user_groups),
        ]

    @http.route(['/my/department_messages', '/my/department_messages/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_department_messages(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='subject', **kw):
        values = self._prepare_my_department_messages_values(page, date_begin, date_end, sortby, filterby, search, groupby, search_in)
        return request.render('tyt_intranet_messaging.portal_my_department_messages', values)

    def _prepare_my_department_messages_values(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='subject'):
        values = self._prepare_portal_layout_values()
        domain = self._prepare_department_messages_domain()
        _items_per_page = 50
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'published_date desc'},
            'sender': {'label': _('Sender'), 'order': 'sender_portal'},
            'subject': {'label': _('Subject'), 'order': 'subject'},
        }
        searchbar_inputs = {
            'sender': {'input': 'sender_portal', 'label': _('Search in Sender')},
            'subject': {'input': 'subject', 'label': _('Search in Subject')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'sender': {'input': 'sender_portal', 'label': _('Sender')},
            'is_read': {'input': 'is_read', 'label': _('Read Status')},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        if groupby in searchbar_groupby and groupby != 'none':
            order = f'{searchbar_groupby[groupby]["input"]}, {order}'

        if search and search_in:
            search_domain = []
            if search_in == 'subject':
                search_domain = OR([search_domain, [('subject', 'ilike', search)]])
            domain = AND([domain, search_domain])

        department_message_count = request.env['tyt.intranet.department_message'].sudo().search_count(domain)
        pager = portal_pager(
            url="/my/department_messages",
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby, 'filterby': filterby},
            total=department_message_count,
            page=page,
            step=_items_per_page,
        )
        department_messages = request.env['tyt.intranet.department_message'].sudo().search(domain, order=order, limit=_items_per_page, offset=pager['offset'])
        for message in department_messages:
            message.is_read = message.is_read_by_current_user()

        if groupby != 'none':
            grouped_department_messages = [request.env['tyt.intranet.department_message'].sudo().concat(*g) for k, g in groupbyelem(department_messages, itemgetter(searchbar_groupby[groupby]['input']))]
        else:
            grouped_department_messages = [department_messages]

        values.update({
            'page_name': 'department_messages',
            'default_url': '/my/department_messages',
            'grouped_department_messages': grouped_department_messages,
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
            'search_in': search_in,
            'search': search,
        })
        return values

    @http.route('/mark_as_read', type='json', auth='user')
    def mark_as_read(self, message_id):
        department_message = request.env['tyt.intranet.department_message'].sudo().browse(message_id)
        if department_message.exists() and not department_message.is_read_by_current_user():
            department_message.mark_as_read_by_current_user()
        return {'success': True}
