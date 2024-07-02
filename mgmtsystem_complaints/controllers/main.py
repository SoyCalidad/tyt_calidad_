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

    @http.route('/reclamo', type='http', auth='public', website=True, sitemap=False)
    def web_course_inscription(self, *args, **kw):
        values = request.params.copy()
        values['reason_ids'] = request.env['complaint.complaint.reason'].sudo().search([
        ])
        values['categ_id'] = request.env['complaint.categ'].sudo().search([])
        print(values['categ_id'])
        response = request.render('mgmtsystem_complaints.complaint', values)
        return response

    @http.route(['/reclamo_enviado'], type='http', methods=['POST'], auth='public', website=True)
    def my_controller_method(self, **kw):
        op_admission_model = request.env['complaint.complaint']
        print(kw)
        file_encoded = b''
        if kw.get('complaint_files'):
            file = kw.get('complaint_files').read()
            file_encoded = base64.b64encode(file)

        real_values = {}

        reason_arr = []

        for val in kw.keys():
            if kw[val]:
                if val == 'complaint_files':
                    real_values[val] = file_encoded
                elif val == 'date_incident':
                    real_values[val] = kw[val].replace('T', ' ')
                elif val == 'reason_other':
                    real_values[val] = kw[val]
                elif 'reason_' in val:
                    reason_arr.append(kw[val])
                elif val == 'categ_id':
                    print (kw[val])
                    real_values['categ_id'] = int(kw['categ_id'])
                elif val == 'type':
                    if kw[val] == 'Interna':
                        real_values[val] = 'customer'
                    elif kw[val] == 'Externa':
                        real_values[val] = 'supplier'
                    if kw.get('type') and kw['type'] == 'Externa':
                        partner_id = request.env['res.partner'].sudo().search(
                            [('name', '=', kw[val])])
                        if partner_id:
                            real_values['partner_id'] = partner_id.id
                    elif kw.get('type') and kw['type'] == 'Interna':
                        employee_id = request.env['hr.employee'].sudo().search(
                            [('name', '=', kw[val])])
                        if employee_id:
                            real_values['employee_notify_id'] = employee_id.id
                elif val == 'complainer_delivery_type':
                    delivery_type_vals = {
                        'Seleccione como quiere recibir la respuesta a tu reclamo': None,
                        'Quiero recibirla por correo electronico': 'email',
                        'Quiero recibirla por celular': 'phone',
                    }
                    real_values[val] = delivery_type_vals[kw[val]]
                else:
                    real_values[val] = kw[val]
                
                complaint_name = kw['name'] + ' ' +  kw['date_incident'].replace('T', ' ')
                real_values['name'] = complaint_name or '-'
                real_values['complainer_name'] = kw['name']

        res_id = op_admission_model.sudo().create(real_values)
        res_id.reason_ids = [(6, 0, reason_arr)]
        response = request.render('mgmtsystem_complaints.complaint_done', {})
        return response
