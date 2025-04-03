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

    is_registered_in_crehana = fields.Boolean(string='¿Está registrado en crehana?')
    is_registered_on_a_learning_path = fields.Boolean(string='¿Está registrado en una ruta de aprendizaje?')

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

        url = "https://www.crehana.com/api/rest/org/demo-tyt-api/users/"
        message = "Problemas con los datos, contacte con su administrador"
        title = "Datos faltantes"

        if not self.work_email:
            message = "No se encontró email de trabajo"

        elif not self.x_studio_nombres or not self.x_studio_apellido_paterno or not self.x_studio_apellido_materno:
            message = "No se econtró el nombre del empleado"
        else:
            headers = {
                "api-key": "6f73522fa7b4eb8c54a1",
                "secret-access": "b65fbff8821dab56651bd23b6142080957a327c13f9e3f543ac3c306a746166e",
                "Content-Type": "application/json"
            }

            payload = {
                "first_name": self.x_studio_nombres,
                "last_name": f"{self.x_studio_apellido_paterno} {self.x_studio_apellido_materno}",
                "email": self.work_email
                # "password": "1234"
            }

            _logger.info(f"payload {payload}")

            try:
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()

                title = "Registrado"
                message = "El empleado fue registrado exitosamente"

                data = response.json()

                self.id_crehana = data.get('id')
                self.is_registered_in_crehana = True

                _logger.info(f"Registrado con el id: {data.get('id')}")
                _logger.info(f"Registrado con el id: {data.get('user')}")

                return {'type': 'ir.actions.client', 'tag': 'reload'}
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise models.ValidationError(f"Error al obtener datos: {e}")

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

    def action_register_on_a_learning_path(self):
        _logger.info("Ejecutando action_register_on_a_learning_path...")

        url = "https://www.crehana.com/api/rest/org/demo-tyt-api/tracks/"
        message = "Problemas con los datos, contacte con su administrador"
        title = "Datos faltantes"

        if not self.id_crehana:
            message = "No se encontró identificador de crehana"
        else:
            headers = {
                "api-key": "6f73522fa7b4eb8c54a1",
                "secret-access": "b65fbff8821dab56651bd23b6142080957a327c13f9e3f543ac3c306a746166e",
                "Content-Type": "application/json"
            }

            payload = {
                "team_id": 17650,
                "user_organization_id": self.id_crehana,
            }

            _logger.info(f"payload {payload}")

            try:
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()

                title = "Registrado"
                message = "El empleado fue registrado exitosamente en la ruta de aprendizaje"

                data = response.json()
                
                _logger.info(f"Registrado {data}")

                return {'type': 'ir.actions.client', 'tag': 'reload'}
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise models.ValidationError(f"Error al obtener datos: {e}")

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

    def action_show_learning_progress(self):
        _logger.info("Ejecutando action_show_learning_progress...")

        url = f"https://www.crehana.com/api/rest/org/demo-tyt-api/course_user_report/{self.id_crehana}/"

        headers = {
            "api-key": "6f73522fa7b4eb8c54a1",
            "secret-access": "b65fbff8821dab56651bd23b6142080957a327c13f9e3f543ac3c306a746166e",
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
                              
            _logger.info(f"employeeeeeeeeeeee {self.id}")
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

    @api.model
    def action_server_get_progress(self):
        _logger.info("into action_progress_total_from_api111111111111")
        # data = self.fetch_progress_total()
        _logger.info("into action_progress_total_from_api222222222222")

        partners = self.env['res.partner'].search([])  # Ejemplo de partners

        workbook = None  # O crea un workbook con xlsxwriter

        data = {
            "records": [
                {"id": 1, "name": "Requisición A", "description": "Descripción A", "created_at": "2025-04-02"},
                {"id": 2, "name": "Requisición B", "description": "Descripción B", "created_at": "2025-04-03"}
            ]
        }

        file_data = self.generate_report_profess(workbook, data, partners)

        # Devolver el archivo en un binario para descargar en Odoo
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=tu.modelo&id=1&field=file_data&download=true',
            'target': 'self',
        }

    @api.model
    def fetch_progress_total(self):
        _logger.info("Ejecutando fetch_names_from_api...")

    def generate_report_profess(self, workbook, data, partners):
        if workbook is None:
            output = BytesIO()
            workbook = xlsxwriter.Workbook(output)

        sheet = workbook.add_worksheet('Reporte de requisición')

        # Formato del título
        title_format = workbook.add_format({
            'font_size': 14,
            'font_name': 'Calibri',
            'bg_color': '#31869B',
            'font_color': 'white',
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'border': 1
        })

        # Formato de las celdas
        cell_format = workbook.add_format({
            'font_size': 12,
            'font_name': 'Calibri',
            'align': 'left',
            'valign': 'vcenter',
            'border': 1
        })

        # Suponiendo que `data` es un diccionario con una lista bajo la clave 'records'
        records = data.get('records', [])

        # Encabezados de la tabla
        headers = ["ID", "Nombre", "Descripción", "Fecha de Creación"]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, title_format)

        # Escribir datos de la lista
        for row, record in enumerate(records, start=1):
            sheet.write(row, 0, record.get('id', ''), cell_format)
            sheet.write(row, 1, record.get('name', ''), cell_format)
            sheet.write(row, 2, record.get('description', ''), cell_format)
            sheet.write(row, 3, record.get('created_at', ''), cell_format)

        return workbook
