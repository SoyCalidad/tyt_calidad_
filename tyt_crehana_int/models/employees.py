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

            if not self.private_email and not self.work_email:
                message = "No se encontró email del empleado"

            if not hasattr(self, 'empleado_nombre') or not hasattr(self, 'empleado_paterno') or not hasattr(self, 'empleado_materno'):
                if self.name:
                    nombres_completos = self.name.strip().split()
                    empleado_nombre = nombres_completos[0] if len(nombres_completos) > 0 else ''
                    empleado_paterno = nombres_completos[1] if len(nombres_completos) > 1 else ''
                    empleado_materno = nombres_completos[2] if len(nombres_completos) > 2 else ''
                else:
                    raise models.ValidationError("El nombre del empleado no está definido correctamente. Por favor, asegúrese de que el campo 'name' esté completo.")
            else:
                empleado_nombre = self.empleado_nombre.strip() if self.empleado_nombre else ''
                empleado_paterno = self.empleado_paterno.strip() if self.empleado_paterno else ''
                empleado_materno = self.empleado_materno.strip() if self.empleado_materno else ''

            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json"
            }

            payload = {
                "first_name": empleado_nombre,
                "last_name": f"{empleado_paterno} {empleado_materno}",
                "email": self.private_email or self.work_email,
                "area_level_1_id": "122564672",
                "position_id": "43849",
                "position_category_id": "55184",
                "headquarter_id": "22524",
                "incorporation_date": self.create_date.strftime('%Y-%m-%d') if self.create_date else ''
            }

            try:
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()

                title = "Registrado"
                message = "El empleado fue registrado exitosamente"

                data = response.json()

                _logger.info(f"Datos obtenidos: {data}")

                self.id_crehana = data.get('id')
                self.user_crehana = data.get('user').get('username')
                self.is_registered_in_crehana = True

                # return {'type': 'ir.actions.client', 'tag': 'reload'}
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

            email = self.private_email or self.work_email

            user_url = f"https://www.crehana.com/api/rest/org/{settings.organization_slug}/users/?email={email}"
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json"
            }

            try:
                response = requests.get(user_url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()

                _logger.info(f"Datos obtenidos: {data}")

                if data and isinstance(data, list) and len(data) > 0:
                    self.id_crehana = data[0].get('id')
                else:
                    _logger.error(f"No se encontró el usuario en Crehana para el email: {email}")
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

                        _logger.info(f"Empleado registrado en la ruta: {data}")

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

    def action_show_user_report(self):

        settings = self.env['tyt_crehana.crehana_settings'].get_first_settings()


        if settings:

            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json"
            }
 
            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/reports/learning/general/?user_email={self.private_email or self.work_email}"

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()

                _logger.info(f"Datos obtenidos para el reporte del empleado: {data}")

                email = self.private_email or self.work_email

                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Reporte del Empleado',
                    'res_model': 'tyt.crehana.general.report',
                    'view_mode': 'tree',
                    'res_id': False,
                    'domain': [('crehana_user_email', '=', email)],
                    'target': 'current',
                }
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise models.ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise models.ValidationError("Error al obtener credenciales de acceso para API's")

    def update_employee_level(self):

        if not self.level:
            _logger.error("El nivel del empleado no está definido.")
            raise models.ValidationError("El nivel del empleado no está definido.")

        settings = self.env['tyt_crehana.crehana_settings'].get_first_settings()

        if settings and self.id_crehana:

            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/{self.id_crehana}/custom_fields/"
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json"
            }

            payload = {
                "custom_fields": [
                    {
                        "id": 1944,
                        "value": self.level or "",
                        "type": "TEXT"
                    }
                ]
            }

            try:
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()

                _logger.info("Nivel PDP actualizado exitosamente")
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al actualizar nivel PDP: {e}")
                raise models.ValidationError(f"Error al actualizar nivel PDP: {e}")
    
    def tyt_crehana_get_employee_level(self):

        settings = self.env['tyt_crehana.crehana_settings'].get_first_settings()

        if settings and self.id_crehana:

            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/reports/learning/general/?user_email={self.private_email or self.work_email}"
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json"
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()

                _logger.info(f"Datos obtenidos para el reporte del empleado: {data}")

                if data and isinstance(data, list) and len(data) > 0:
                    custom_fields = data[0].get('custom_fields', [])
                    for field in custom_fields:
                        if field.get('id') == 1944:
                            self.level = field.get('value')
                            _logger.info(f"Nivel del empleado actualizado a: {self.level}")
                            break
                else:
                    _logger.error(f"No se encontró el reporte en Crehana para el email: {self.private_email or self.work_email}")
                    raise models.ValidationError("No se encontró el reporte o el nivel del empleado en Crehana para el email proporcionado.")
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise models.ValidationError(f"Error al obtener datos: {e}")
