from odoo import http
from odoo.http import request, Response
import json

class PublicFormController(http.Controller):
    
    @http.route('/employee/update', type='http', auth='public')
    def list_fields_departments(self):

        departments_temp = request.env['hr.department'].sudo().search([])

        for department in departments_temp:

            if str(department.master_department_id.name) == 'Mtya':
                department.days = 12

    @http.route('/testing_names/list', type='http', auth='public')
    def name_list(self):
        json_data = []
        for i in range(10):  # Corrección del bucle
            json_data.append({
                'name': f"asdfasdf{i}"  # Corrección de la f-string
            })

        return Response(
            json.dumps(json_data),
            content_type='application/json;charset=utf-8'
        )
    