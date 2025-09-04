# -*- coding: utf-8 -*-
import requests
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class LearningPath(models.Model):
    _name = 'tyt_crehana.learning_path'
    _description = 'Rutas de aprendizaje'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Nombre', tracking=True)
    id_path = fields.Char(string='Identificador de ruta', tracking=True)

    course_ids = fields.One2many('tyt_crehana.learning_path_course', 'path_id', string="Cursos")

    @api.model
    def action_fetch_paths_from_api(self):
        _logger.info("into action_fetch_paths_from_api")
        self.fetch_paths_from_api()

        return {
            'name': 'Lista de rutas de aprendizaje',
            'type': 'ir.actions.act_window',
            'res_model': 'tyt_crehana.learning_path',
            'view_mode': 'tree',
            'view_id': self.env.ref('tyt_crehana_int.tyt_crehana_learning_path_tree_view').id,
            'target': 'current'
        }

    @api.model
    def fetch_paths_from_api(self):
        _logger.info("Ejecutando fetch_names_from_api...")

        settings = self.env['tyt_crehana.crehana_settings'].get_first_settings()

        if settings:
            url = f"https://www.crehana.com/api/rest/org/{settings.organization_slug}/"
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json"
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()

                for item in data.get('tracks', []):

                    id_path = item.get('id')
                    if not id_path:
                        continue

                    path = self.env['tyt_crehana.learning_path'].search([
                        ('id_path', '=', id_path)
                    ], limit=1)

                    if not path:
                        new_data = {
                            'id_path': id_path,
                            'name': item.get('name', 'Sin Nombre')
                        }
                        path = self.env['tyt_crehana.learning_path'].create(new_data)   

                    existing_course_ids = path.course_ids.mapped('id_course')
                    courses_to_create = []

                    for course in item.get('courses', []):

                        course_id = course.get('id')
                        if not course_id:
                            continue

                        if course_id not in existing_course_ids:
                            new_data_course = {
                                'id_course': course_id,
                                'title': course.get('title', 'Sin Nombre'),
                                'path_id': path.id
                            }
                            courses_to_create.append(new_data_course)
                    if courses_to_create:
                        self.env['tyt_crehana.learning_path_course'].create(courses_to_create)

            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise ValidationError("Error al obtener credenciales de acceso para API's")
        return True

class LearningPathCourse(models.Model):
    _name = 'tyt_crehana.learning_path_course'
    _description = 'Curso de aprendizaje'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'

    title = fields.Char(string='Título', tracking=True)
    id_course = fields.Char(string='Identificador del curso', tracking=True)

    path_id = fields.Many2one('tyt_crehana.learning_path', string="Ruta de aprendizaje")

class LearningCourse(models.Model):
    _name = 'tyt_crehana.learning_course'
    _description = 'Avances por curso'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Título', tracking=True)
    id_course = fields.Char(string='Identificador del curso', tracking=True)
    hours = fields.Char(string='Horas avanzadas', tracking=True)
    progress = fields.Char(string='Progreso', tracking=True)
    level_of_employee = fields.Char(string='Nivel del empleado', tracking=True)
    job_of_employee = fields.Char(string='Posición del empleado', tracking=True)

    employee_id = fields.Many2one('hr.employee', string="Empleado", tracking=True)
    path_id = fields.Many2one('tyt_crehana.learning_path', string="Ruta de trabajo", tracking=True)
