import logging

from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.http import request, route
from odoo.tools.translate import _
from odoo.osv.expression import OR, AND


class BirthdayPublicationPortal(portal.CustomerPortal):

    @route(['/my', '/my/home'], type='http', auth='user', website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        show_birthday_card_modal = True
        employee = request.env.user.x_studio_empleado
        if employee and employee.birthday_publication_ids:
            if request.session.get('birthday_card_modal_shown'):
                show_birthday_card_modal = False
            else:
                request.session['birthday_card_modal_shown'] = True
        else:
            show_birthday_card_modal = False
        values.update({
            'show_birthday_card_modal': show_birthday_card_modal,
        })
        return request.render("tyt_intranet_birthday.portal_my_home", values)

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        domain = self._prepare_birthday_publication_domain()
        if 'birthday_publication_count' in counters:
            values['birthday_publication_count'] = request.env['hr.employee'].sudo().search_count(domain)
        return values

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        return values

    def _prepare_birthday_publication_domain(self):
        employee = request.env.user.x_studio_empleado
        return [
            ('include_in_birthday_publication', '=', True),
            ('birthday', '!=', False),
            ('is_birthday', '=', True),
            ('x_studio_sitios0', '!=', False),
            '|',
            ('include_in_all_birthday_publications', '=', True),
            ('x_studio_sitios0.id', '=', employee.x_studio_sitios0.id),
        ]

    @http.route(['/birthday_publication', '/birthday_publication/page/<int:page>'], type='http', auth='user', website=True)
    def portal_birthday_publication(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='today', search=None, groupby='none', search_in='name', **kw):
        values = self._prepare_birthday_publication_values(page, date_begin, date_end, sortby, filterby, search, groupby, search_in)
        return request.render('tyt_intranet_birthday.portal_birthday_publication', values)

    def _prepare_birthday_publication_values(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='today', search=None, groupby='none', search_in='name'):
        values = self._prepare_portal_layout_values()
        domain = self._prepare_birthday_publication_domain()
        searchbar_filters = {
            'today': {'label': _('Today'), 'domain': [('is_birthday', '!=', False)]},
            'this_week': {'label': _('This Week'), 'domain': [('is_birthday_this_week', '!=', False)]},
            'this_month': {'label': _('This Month'), 'domain': [('is_birthday_this_month', '!=', False)]},
        }
        if filterby in ['this_week', 'this_month']:
            if ('is_birthday', '=', True) in domain:
                domain.remove(('is_birthday', '=', True))
        domain = AND([domain, searchbar_filters[filterby]['domain']])
        employees = request.env['hr.employee'].sudo().search(domain, order='name')
        values.update({
            'page_name': 'birthday_publication',
            'default_url': '/birthday_publication',
            'employees': employees,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
        })
        return values
