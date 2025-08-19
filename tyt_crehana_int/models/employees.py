# -*- coding: utf-8 -*-
import requests
from odoo import api, models, fields

import xlsxwriter
from io import BytesIO

import logging
_logger = logging.getLogger(__name__)

class EmployeeExtension(models.Model):
    _inherit = 'hr.employee'

    id_crehana = fields.Char(string='Identificacdor Crehana')
    user_crehana = fields.Char(string='Username')
    level = fields.Selection(
        [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        string='Nivel',
        required=False,
    )

    is_registered_in_crehana = fields.Boolean(string='¿Está registrado en crehana?', tracking=True)
    is_registered_on_a_learning_path = fields.Boolean(string='¿Está registrado en una ruta de aprendizaje?', tracking=True)

    course_ids = fields.One2many('tyt_crehana.learning_course', 'employee_id', string="Cursos")
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self.env.context

        if context.get('default_dynamic_domain'):
            positions = self.env['tyt_crehana.job_positions'].sudo().search([])
            
            job_ids = positions.mapped('job_id.id')
            levels = []
            if any(positions.mapped('level_a')): levels.append('A')
            if any(positions.mapped('level_b')): levels.append('B')
            if any(positions.mapped('level_c')): levels.append('C')
            if any(positions.mapped('level_d')): levels.append('D')

            if job_ids:
                args.append(('job_id', 'in', job_ids))
            if levels:
                args.append(('level', 'in', levels))

        return super().search(args, offset=offset, limit=limit, order=order, count=count)
    
    def action_register_in_crehana(self):
        _logger.info("Ejecutando action_register_in_crehana...")

        settings = self.env['tyt_crehana.crehana_settings'].get_first_settings()

        if settings:

            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/"
            message = "Problemas con los datos, contacte con su administrador"
            title = "Datos faltantes"

            if not self.work_email:
                message = "No se encontró email de trabajo"

            elif not self.empleado_nombre or not self.empleado_paterno or not self.empleado_materno:
                message = "No se econtró el nombre del empleado"
            else:
                headers = {
                    "api-key": settings.api_key,
                    "secret-access": settings.secret_access,
                    "Content-Type": "application/json"
                }

                payload = {
                    "first_name": self.empleado_nombre,
                    "last_name": f"{self.empleado_paterno} {self.empleado_materno}",
                    "email": self.work_email,
                    "area_level_1_id": "",
                    "position_id": "",
                    "position_category_id": "",
                    "headquarter_id": "",
                    "incorporation_date": "",
                    # "password": "1234"
                }

                try:
                    response = requests.post(url, json=payload, headers=headers, timeout=10)
                    response.raise_for_status()

                    title = "Registrado"
                    message = "El empleado fue registrado exitosamente"

                    data = response.json()

                    self.id_crehana = data.get('id')
                    self.user_crehana = data.get('user').get('username')
                    self.is_registered_in_crehana = True

                    return {'type': 'ir.actions.client', 'tag': 'reload'}
                except requests.exceptions.RequestException as e:
                    _logger.error(f"Error al obtener datos: {e}")
                    raise models.ValidationError(f"Error al obtener datos: {e}")

                # Actualizar nivel PDP del empleado

                pdp_custom_fields_url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/{self.id_crehana}/custom_fields/"
                pdp_custom_fields_payload = {
                    "custom_fields": [
                        {
                            "id": 1944,
                            "value": self.level or "",
                            "type": "TEXT"
                        }
                    ]
                }

                try:
                    custom_fields_response = requests.post(pdp_custom_fields_url, json=pdp_custom_fields_payload, headers=headers, timeout=10)
                    custom_fields_response.raise_for_status()

                    _logger.info("Campos personalizados actualizados exitosamente")
                except requests.exceptions.RequestException as e:
                    _logger.error(f"Error al actualizar campos personalizados: {e}")
                    raise models.ValidationError(f"Error al actualizar campos personalizados: {e}")

                # Actualizar el número del empleado

                emp_number_custom_fields_url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/{self.id_crehana}/custom_fields/"
                emp_number_custom_fields_payload = {
                    "custom_fields": [
                        {
                            "id": 1942,
                            "value": str(self.id),
                            "type": "TEXT"
                        }
                    ]
                }

                try:
                    emp_number_response = requests.post(emp_number_custom_fields_url, json=emp_number_custom_fields_payload, headers=headers, timeout=10)
                    emp_number_response.raise_for_status()

                    _logger.info("Número de empleado actualizado exitosamente")
                except requests.exceptions.RequestException as e:
                    _logger.error(f"Error al actualizar el número de empleado: {e}")
                    raise models.ValidationError(f"Error al actualizar el número de empleado: {e}")

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': title,
                    'message': message,
                    'type': 'success',  
                    'sticky': False
                }
            }

        else:
            _logger.error(f"Error de credenciales de acceso")
            raise models.ValidationError("Error al obtener credenciales de acceso para API's")

    def action_register_on_a_learning_path(self):
        _logger.info("Ejecutando action_register_on_a_learning_path...")

        settings = self.env['tyt_crehana.crehana_settings'].get_first_settings()

        if settings:

            # Obtener los datos del usuario y el id centralizado

            user_url = f"https://www.crehana.com/api/rest/org/{settings.organization_slug}/users/?email={self.work_email}"
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json"
            }

            try:
                response = requests.get(user_url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()

                if data and isinstance(data, list) and len(data) > 0:
                    self.id_crehana = data[0].get('id')
                else:
                    _logger.error(f"No se encontró el usuario en Crehana para el email: {self.work_email}")
                    raise models.ValidationError("No se encontró el usuario en Crehana para el email proporcionado.")
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise models.ValidationError(f"Error al obtener datos: {e}")

            url = f"https://www.crehana.com/api/rest/org/{settings.organization_slug}/tracks/"
            message = "Problemas con los datos, contacte con su administrador"
            title = "Datos faltantes"

            if not self.id_crehana:
                message = "No se encontró identificador de crehana"
            else:
                headers = {
                    "api-key": settings.api_key,
                    "secret-access": settings.secret_access,
                    "Content-Type": "application/x-www-form-urlencoded"
                }

                # Obtener ruta para su posición
                position = self.env['tyt_crehana.job_positions'].sudo().search([
                    ('job_id', '=', self.job_id.id)
                ])

                path_selected = None
                if position.level_a and self.level == 'A':
                    path_selected = position.path_to_position_a
                elif position.level_b and self.level == 'B':
                    path_selected = position.path_to_position_b
                elif position.level_c and self.level == 'C':
                    path_selected = position.path_to_position_c
                elif position.level_d and self.level == 'D':
                    path_selected = position.path_to_position_d

                if path_selected and path_selected.id_path:

                    data = {
                        "team_id": str(path_selected.id_path),
                        "user_organization_id": str(self.id_crehana),
                    }

                    try:
                        response = requests.post(url, data=data, headers=headers, timeout=10)
                        response.raise_for_status()

                        title = "Registrado"
                        message = "El empleado fue registrado exitosamente en la ruta de aprendizaje"

                        data = response.json()

                        self.is_registered_on_a_learning_path = True

                        return {'type': 'ir.actions.client', 'tag': 'reload'}
                    except requests.exceptions.RequestException as e:
                        _logger.error(f"Error al obtener datos: {e}")
                        raise models.ValidationError(f"Error al obtener datos: {e}")
                else:
                    title = "Error"
                    message = "El empleado tiene problemas con su posición y/o nivel, contacte con un administrador."

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': title,
                    'message': message,
                    'type': 'success',  
                    'sticky': False
                }
            }
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise models.ValidationError("Error al obtener credenciales de acceso para API's")

    def action_show_learning_progress(self):
        _logger.info("Ejecutando action_show_learning_progress...")

        settings = self.env['tyt_crehana.crehana_settings'].get_first_settings()

        if settings:
            url = f"https://www.crehana.com/api/rest/org/{settings.organization_slug}/course_user_report/{self.id_crehana}/"

            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json"
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()

                for item in data:

                    data_course = item.get('course', {})
                    if not data_course:
                        continue

                    course_info = data_course.get('course', {})
                    course_id = course_info.get('id')
                    course_title = course_info.get('title')

                    if not course_id or not course_title:
                        continue

                    new_data = {
                        "hours": item.get('hours', '0'),
                        "progress": item.get('progress', '0')
                    }

                    course = self.env['tyt_crehana.learning_course'].search([
                        ('id_course', '=', course_id),
                        ('employee_id', '=', self.id)
                    ], limit=1)

                    if course:
                        course.write(new_data)

                    else:
                        new_data["id_course"] = course_id
                        new_data["name"] = course_title
                        new_data["employee_id"] = self.id
                        new_data["level_of_employee"] = self.level
                        new_data["job_of_employee"] = self.job_id.name

                        self.env['tyt_crehana.learning_course'].create(new_data)   
                                
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Cursos del Empleado',
                    'res_model': 'hr.employee',
                    'view_mode': 'form',
                    'view_id': self.env.ref('tyt_crehana_int.view_crehana_employee_courses_form').id,
                    'res_id': self.id,
                    'context': {'default_employee_id': self.id},
                    'target': 'current'
                }

            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise models.ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise models.ValidationError("Error al obtener credenciales de acceso para API's")