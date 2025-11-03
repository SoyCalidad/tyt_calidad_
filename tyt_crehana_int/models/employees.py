# -*- coding: utf-8 -*-
import requests
from odoo import api, models, fields
from odoo.exceptions import ValidationError

import xlsxwriter
from io import BytesIO

import logging

_logger = logging.getLogger(__name__)


class EmployeeExtension(models.Model):
    _inherit = 'hr.employee'

    id_crehana = fields.Char(string='Identificacdor Crehana')
    user_crehana = fields.Char(string='Username')
    level = fields.Selection(
        [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
        string="Nivel",
        required=False,
    )

    is_registered_in_crehana = fields.Boolean(
        string="¿Está registrado en crehana?", tracking=True
    )
    is_registered_on_a_learning_path = fields.Boolean(
        string="¿Está registrado en una ruta de aprendizaje?", tracking=True
    )

    course_ids = fields.One2many(
        "tyt_crehana.learning_course", "employee_id", string="Cursos"
    )

    # Other fields

    cliente = fields.Char(string="Cliente")
    centros = fields.Char(string="Centros")
    especialidades = fields.Char(string="Especialidades")
    generacion = fields.Char(string="Generación")
    perfil = fields.Char(string="Perfil")
    no_empleado = fields.Text(string="No. de Empleado")
    proyecto_asignado_1 = fields.Char(string="Proyecto Asignado 1")
    puesto = fields.Char(string="Puesto")
    area = fields.Char(string="Área")
    proyecto_asignado_2 = fields.Char(string="Proyecto Asignado 2")
    campanas = fields.Char(string="Campañas")
    nivel_pdp = fields.Char(string="Nivel de PDP")
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    turnos = fields.Char(string="Turnos")
    fecha_ingreso = fields.Date(string="Fecha de Ingreso")
    sexo = fields.Char(string="Sexo")
    crehana_email = fields.Char(string="Email Crehana")

    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        context = self.env.context

        if context.get("default_dynamic_domain"):
            positions = self.env["tyt_crehana.job_positions"].sudo().search([])

            job_ids = positions.mapped("job_id.id")
            levels = []
            if any(positions.mapped("level_a")):
                levels.append("A")
            if any(positions.mapped("level_b")):
                levels.append("B")
            if any(positions.mapped("level_c")):
                levels.append("C")
            if any(positions.mapped("level_d")):
                levels.append("D")

            if job_ids:
                args.append(("job_id", "in", job_ids))
            if levels:
                args.append(("level", "in", levels))

        return super().search(
            args, offset=offset, limit=limit, order=order
        )

    def _get_custom_fields_mapping(self):
        """
        Mapeo de campos Odoo a IDs de campos personalizados de Crehana
        """
        return {
            1936: {"field": "cliente", "type": "MULTIPLE"},
            1941: {"field": "centros", "type": "MULTIPLE"},
            1946: {"field": "especialidades", "type": "MULTIPLE"},
            1951: {"field": "generacion", "type": "MULTIPLE"},
            1937: {"field": "perfil", "type": "MULTIPLE"},
            1942: {"field": "no_empleado", "type": "TEXT"},
            1947: {"field": "proyecto_asignado_1", "type": "MULTIPLE"},
            1938: {"field": "puesto", "type": "MULTIPLE"},
            1943: {"field": "area", "type": "MULTIPLE"},
            1948: {"field": "proyecto_asignado_2", "type": "MULTIPLE"},
            1939: {"field": "campanas", "type": "MULTIPLE"},
            1944: {
                "field": "nivel_pdp",
                "type": "MULTIPLE",
            },
            1949: {"field": "fecha_nacimiento", "type": "DATE"},
            1940: {"field": "turnos", "type": "MULTIPLE"},
            1945: {"field": "fecha_ingreso", "type": "DATE"},
            1950: {"field": "sexo", "type": "MULTIPLE"},
        }

    def _prepare_custom_fields_payload(self, field_ids=None):
        """
        Prepara el payload para enviar campos personalizados a Crehana

        :param field_ids: Lista de IDs de campos específicos a enviar. Si es None, envía todos.
        :return: Payload formateado para la API
        """
        mapping = self._get_custom_fields_mapping()
        custom_fields = []

        fields_to_process = field_ids or mapping.keys()

        for field_id in fields_to_process:
            if field_id not in mapping:
                continue

            field_config = mapping[field_id]
            field_name = field_config["field"]
            field_type = field_config["type"]

            # Obtener valor del campo
            field_value = getattr(self, field_name, None)

            # Manejar campos especiales
            if field_name == "nivel_pdp" and not field_value:
                # Mantener compatibilidad con el campo 'level' existente
                field_value = getattr(self, "level", "")
            elif field_name == "no_empleado" and not field_value:
                # Usar el ID del empleado como fallback
                field_value = str(self.id)

            # Formatear valor según el tipo
            if field_type == "DATE" and field_value:
                if isinstance(field_value, str):
                    formatted_value = field_value
                else:
                    formatted_value = field_value.strftime("%d-%m-%Y")
            elif field_type == "MULTIPLE":
                # Para campos MULTIPLE, enviar como string pero puede contener múltiples valores separados
                formatted_value = str(field_value) if field_value else ""
            else:  # TEXT
                formatted_value = str(field_value) if field_value else ""

            custom_fields.append(
                {"id": field_id, "value": formatted_value, "type": field_type}
            )

        return {"custom_fields": custom_fields}

    def _send_custom_fields_to_crehana(self, field_ids=None):
        """
        Envía campos personalizados a Crehana

        :param field_ids: Lista de IDs de campos específicos a enviar
        :return: True si fue exitoso, False en caso contrario
        """
        if not self.id_crehana:
            _logger.warning(f"Empleado {self.name} no tiene ID de Crehana registrado")
            return False

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()
        if not settings:
            _logger.error("No se encontraron credenciales de Crehana")
            return False

        url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/{self.id_crehana}/custom-fields/"

        headers = {
            "api-key": settings.api_key,
            "secret-access": settings.secret_access,
            "Content-Type": "application/json",
        }

        payload = self._prepare_custom_fields_payload(field_ids)

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()

            _logger.info(
                f"Campos personalizados enviados exitosamente para empleado {self.name} {response}"
            )
            return True

        except requests.exceptions.RequestException as e:
            _logger.error(
                f"Error al enviar campos personalizados para {self.name}: {e} {response}"
            )
            return False

    def action_register_in_crehana(self):
        _logger.info("Ejecutando action_register_in_crehana...")

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        if settings:
            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/"
            message = "Problemas con los datos, contacte con su administrador"
            title = "Datos faltantes"

            if not self.private_email and not self.work_email:
                message = "No se encontró email del empleado"

            if (
                not hasattr(self, "empleado_nombre")
                or not hasattr(self, "empleado_paterno")
                or not hasattr(self, "empleado_materno")
            ):
                if self.name:
                    nombres_completos = self.name.strip().split()
                    empleado_nombre = (
                        nombres_completos[0] if len(nombres_completos) > 0 else ""
                    )
                    empleado_paterno = (
                        nombres_completos[1] if len(nombres_completos) > 1 else ""
                    )
                    empleado_materno = (
                        nombres_completos[2] if len(nombres_completos) > 2 else ""
                    )
                else:
                    raise ValidationError(
                        "El nombre del empleado no está definido correctamente. Por favor, asegúrese de que el campo 'name' esté completo."
                    )
            else:
                empleado_nombre = (
                    self.empleado_nombre.strip() if self.empleado_nombre else ""
                )
                empleado_paterno = (
                    self.empleado_paterno.strip() if self.empleado_paterno else ""
                )
                empleado_materno = (
                    self.empleado_materno.strip() if self.empleado_materno else ""
                )

            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            payload = {
                "first_name": empleado_nombre,
                "last_name": f"{empleado_paterno} {empleado_materno}",
                "email": self.private_email or self.work_email,
                "area_level_1_id": "122564672",
                "position_id": "43849",
                "position_category_id": "55184",
                "headquarter_id": "22524",
                "incorporation_date": (
                    self.create_date.strftime("%Y-%m-%d") if self.create_date else ""
                ),
            }

            _logger.info(
                f"Registrando empleado en Crehana con los siguientes datos: {payload}"
            )

            try:
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()

                title = "Registrado"
                message = "El empleado fue registrado exitosamente"

                data = response.json()

                _logger.info(f"Datos obtenidos: {data}")

                self.id_crehana = data.get("id")
                self.user_crehana = (
                    data.get("user").get("username") if data.get("user") else ""
                )
                self.is_registered_in_crehana = True

            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise ValidationError(f"Error al obtener datos: {e}")

            # Enviar TODOS los campos personalizados
            if self._send_custom_fields_to_crehana():
                _logger.info(
                    "Todos los campos personalizados fueron enviados exitosamente"
                )
            else:
                _logger.warning(
                    "Hubo problemas al enviar algunos campos personalizados"
                )

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": title,
                    "message": message,
                    "type": "success",
                    "sticky": False,
                },
            }

        else:
            _logger.error(f"Error de credenciales de acceso")
            raise ValidationError(
                "Error al obtener credenciales de acceso para API's"
            )

    def action_sync_custom_fields_crehana(self):
        """
        Acción independiente para sincronizar solo los campos personalizados
        """
        if not self.id_crehana:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Error",
                    "message": "El empleado no está registrado en Crehana",
                    "type": "warning",
                    "sticky": False,
                },
            }

        success = self._send_custom_fields_to_crehana()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Sincronización" if success else "Error",
                "message": (
                    "Campos personalizados sincronizados exitosamente"
                    if success
                    else "Error al sincronizar campos personalizados"
                ),
                "type": "success" if success else "danger",
                "sticky": False,
            },
        }

    def action_sync_specific_fields_crehana(self, field_names):
        """
        Sincroniza campos específicos por nombre

        :param field_names: Lista de nombres de campos a sincronizar
        :return: Resultado de la operación
        """
        mapping = self._get_custom_fields_mapping()

        # Convertir nombres de campos a IDs
        field_ids = []
        for field_id, config in mapping.items():
            if config["field"] in field_names:
                field_ids.append(field_id)

        if not field_ids:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "Advertencia",
                    "message": "No se encontraron campos válidos para sincronizar",
                    "type": "warning",
                    "sticky": False,
                },
            }

        success = self._send_custom_fields_to_crehana(field_ids)

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Sincronización" if success else "Error",
                "message": (
                    f"Campos {field_names} sincronizados exitosamente"
                    if success
                    else f"Error al sincronizar campos {field_names}"
                ),
                "type": "success" if success else "danger",
                "sticky": False,
            },
        }

    def action_register_on_a_learning_path(self):
        _logger.info("Ejecutando action_register_on_a_learning_path...")

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        if settings:

            # Obtener los datos del usuario y el id centralizado

            email = self.crehana_email or self.work_email or self.private_email

            user_url = f"https://www.crehana.com/api/rest/org/{settings.organization_slug}/users/?email={email}"
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            try:
                response = requests.get(user_url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()

                _logger.info(f"Datos obtenidos: {data}")

                if data and isinstance(data, list) and len(data) > 0:
                    self.id_crehana = data[0].get("id")
                else:
                    _logger.error(
                        f"No se encontró el usuario en Crehana para el email: {email}"
                    )
                    raise ValidationError(
                        "No se encontró el usuario en Crehana para el email proporcionado."
                    )
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise ValidationError(f"Error al obtener datos: {e}")

            url = f"https://www.crehana.com/api/rest/org/{settings.organization_slug}/tracks/"
            message = "Problemas con los datos, contacte con su administrador"
            title = "Datos faltantes"

            if not self.id_crehana:
                message = "No se encontró identificador de crehana"
            else:
                headers = {
                    "api-key": settings.api_key,
                    "secret-access": settings.secret_access,
                    "Content-Type": "application/x-www-form-urlencoded",
                }

                # Obtener ruta para su posición
                # Mapeo de niveles a campos
                # Mapeo de niveles a dominios de búsqueda y campos de path
                level_mapping = {
                    "A": (
                        [("job_id", "=", self.job_id.id), ("level_a", "=", True)],
                        "path_to_position_a",
                    ),
                    "B": (
                        [("job_id", "=", self.job_id.id), ("level_b", "=", True)],
                        "path_to_position_b",
                    ),
                    "C": (
                        [("job_id", "=", self.job_id.id), ("level_c", "=", True)],
                        "path_to_position_c",
                    ),
                    "D": (
                        [("job_id", "=", self.job_id.id), ("level_d", "=", True)],
                        "path_to_position_d",
                    ),
                }

                path_selected = None
                if self.nivel_pdp and self.nivel_pdp.upper() in level_mapping:
                    level_config = level_mapping.get(self.nivel_pdp.upper())
                else:
                    level_config = ""

                if level_config:
                    domain, path_field = level_config

                    position = (
                        self.env["tyt_crehana.job_positions"]
                        .sudo()
                        .search(domain, limit=1)
                    )

                    if position:
                        path_selected = getattr(position, path_field, None)

                if path_selected and path_selected.id_path:

                    data = {
                        "team_id": str(path_selected.id_path),
                        "user_organization_id": str(self.id_crehana),
                    }

                    try:
                        response = requests.post(
                            url, data=data, headers=headers, timeout=10
                        )
                        response.raise_for_status()

                        title = "Registrado"
                        message = "El empleado fue registrado exitosamente en la ruta de aprendizaje"

                        data = response.json()

                        _logger.info(f"Empleado registrado en la ruta: {data}")

                        self.is_registered_on_a_learning_path = True

                        return {"type": "ir.actions.client", "tag": "reload"}
                    except requests.exceptions.RequestException as e:
                        _logger.error(f"Error al obtener datos: {e}")
                        raise ValidationError(f"Error al obtener datos: {e}")
                else:
                    title = "Error"
                    message = "El empleado tiene problemas con su posición y/o nivel, contacte con un administrador."

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": title,
                    "message": message,
                    "type": "success",
                    "sticky": False,
                },
            }
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise ValidationError(
                "Error al obtener credenciales de acceso para API's"
            )

    def action_show_learning_progress(self):
        _logger.info("Ejecutando action_show_learning_progress...")

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        if settings:
            url = f"https://www.crehana.com/api/rest/org/{settings.organization_slug}/course_user_report/{self.id_crehana}/"

            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()

                for item in data:

                    data_course = item.get("course", {})
                    if not data_course:
                        continue

                    course_info = data_course.get("course", {})
                    course_id = course_info.get("id")
                    course_title = course_info.get("title")

                    if not course_id or not course_title:
                        continue

                    new_data = {
                        "hours": item.get("hours", "0"),
                        "progress": item.get("progress", "0"),
                    }

                    course = self.env["tyt_crehana.learning_course"].search(
                        [("id_course", "=", course_id), ("employee_id", "=", self.id)],
                        limit=1,
                    )

                    if course:
                        course.write(new_data)

                    else:
                        new_data["id_course"] = course_id
                        new_data["name"] = course_title
                        new_data["employee_id"] = self.id
                        new_data["level_of_employee"] = (
                            self.nivel_pdp.upper() if self.nivel_pdp else None
                        )
                        new_data["job_of_employee"] = self.job_id.name

                        self.env["tyt_crehana.learning_course"].create(new_data)

                return {
                    "type": "ir.actions.act_window",
                    "name": "Cursos del Empleado",
                    "res_model": "hr.employee",
                    "view_mode": "form",
                    "view_id": self.env.ref(
                        "tyt_crehana_int.view_crehana_employee_courses_form"
                    ).id,
                    "res_id": self.id,
                    "context": {"default_employee_id": self.id},
                    "target": "current",
                }

            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise ValidationError(
                "Error al obtener credenciales de acceso para API's"
            )

    def action_show_user_report(self):
        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        email = self.crehana_email or self.work_email
        url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/reports/learning/general/?user_email={email}"
        headers = {
            "api-key": settings.api_key,
            "secret-access": settings.secret_access,
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            _logger.info(
                f"Datos obtenidos para el usuario {email}: {len(data.get('results', []))} registros"
            )

            # Obtener registros existentes para este usuario
            existing_records = self.env["tyt.crehana.general.report"].search(
                [("crehana_user_email", "=", email)]
            )
            existing_dict = {}
            for record in existing_records:
                key = f"{record.crehana_user_id}_{record.creahana_course_id}"
                existing_dict[key] = record

            records_to_create = []
            records_to_update = []

            for result in data.get("results", []):
                key = f"{result.get('user_id')}_{result.get('course_id')}"
                custom_fields_str = (
                    str(result.get("user_custom_fields", []))
                    if result.get("user_custom_fields")
                    else ""
                )

                record_data = {
                    "crehana_user_id": result.get("user_id"),
                    "crehana_user_name": result.get("user_name"),
                    "crehana_user_email": result.get("user_email"),
                    "crehana_user_status": result.get("user_status"),
                    "crehana_user_info_extra": result.get("user_info_extra"),
                    "crehana_is_enroll_active": result.get("is_enroll_active", False),
                    "creahana_course_id": result.get("course_id"),
                    "creahana_course_name": result.get("course_name"),
                    "creahana_course_category": result.get("course_category"),
                    "creahana_course_subcategory": result.get("course_subcategory"),
                    "creahana_is_admin_assigned": result.get(
                        "is_admin_assigned", False
                    ),
                    "creahana_assigned_by_name": result.get("assigned_by_name"),
                    "creahana_course_type": result.get("course_type"),
                    "creahana_course_is_reward": result.get("course_is_reward"),
                    "creahana_course_duration_hours": result.get(
                        "course_duration_hours", 0.0
                    ),
                    "creahana_course_progress": result.get("course_progress", 0.0),
                    "creahana_course_progress_hours": result.get(
                        "course_progress_hours", 0.0
                    ),
                    "creahana_course_is_completed": result.get(
                        "course_is_completed", False
                    ),
                    "creahana_project_status": result.get("project_status"),
                    "creahana_project_date": self._parse_date(
                        result.get("project_date")
                    ),
                    "creahana_quiz_status": result.get("quiz_status"),
                    "creahana_quiz_attempts": result.get("quiz_attemps"),
                    "creahana_quiz_best_correct_answers": result.get(
                        "quiz_best_correct_answers"
                    ),
                    "creahana_quiz_best_wrong_answers": result.get(
                        "quiz_best_wrong_answers"
                    ),
                    "creahana_quiz_total_questions": result.get("quiz_total_questions"),
                    "creahana_quiz_best_result": result.get("quiz_best_result"),
                    "creahana_course_is_certified": result.get(
                        "course_is_certified", False
                    ),
                    "creahana_course_has_participation_certificate": result.get(
                        "course_has_participation_certificate", False
                    ),
                    "creahana_course_enroll_date": self._parse_date(
                        result.get("course_enroll_date")
                    ),
                    "creahana_course_start_date": self._parse_date(
                        result.get("course_start_date")
                    ),
                    "creahana_course_complete_date": self._parse_date(
                        result.get("course_complete_date")
                    ),
                    "creahana_project_url": result.get("project_url"),
                    "creahana_course_certificated_url": result.get(
                        "course_certificated_url"
                    ),
                    "creahana_course_participation_certificate_url": result.get(
                        "course_participation_certificate_url"
                    ),
                    "creahana_course_certificated_date": self._parse_date(
                        result.get("course_certificated_date")
                    ),
                    "creahana_course_last_action_date": self._parse_date(
                        result.get("course_last_action_date")
                    ),
                    "creahana_user_division": result.get("user_division"),
                    "creahana_user_subsidiary": result.get("user_subsidiary"),
                    "creahana_user_job": result.get("user_job"),
                    "creahana_user_level": result.get("user_level"),
                    "creahana_user_role": result.get("user_role"),
                    "creahana_track_id": result.get("track_id"),
                    "creahana_track_name": result.get("track_name"),
                    "creahana_track_is_hidden": result.get("track_is_hidden", False),
                    "creahana_user_custom_fields": custom_fields_str,
                }

                if key in existing_dict:
                    records_to_update.append((existing_dict[key], record_data))
                else:
                    records_to_create.append(record_data)

            if records_to_create:
                self.env["tyt.crehana.general.report"].create(records_to_create)
                _logger.info(
                    f"Se crearon {len(records_to_create)} nuevos registros para {email}"
                )

            if records_to_update:
                for record, data in records_to_update:
                    record.write(data)
                _logger.info(
                    f"Se actualizaron {len(records_to_update)} registros para {email}"
                )

            return {
                "type": "ir.actions.act_window",
                "name": "Reporte del Empleado",
                "res_model": "tyt.crehana.general.report",
                "view_mode": "list",
                "domain": [("crehana_user_email", "=", email)],
                "target": "current",
            }
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error al obtener datos para {email}: {e}")
            raise ValidationError(f"Error al obtener datos: {e}")

    def retrieve_crehana_users(self):
        url = f"https://www.crehana.com/api/v5/rest/org/{self.organization_slug}/users/"

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        if settings:
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()
                return data

            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise ValidationError(
                "Error al obtener credenciales de acceso para API's"
            )

    def retrieve_user_by_email(self):

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        if settings:
            email = self.private_email or self.work_email
            url = f"https://www.crehana.com/api/rest/org/{settings.organization_slug}/users/?email={email}"

            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()
                return data

            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise ValidationError(
                "Error al obtener credenciales de acceso para API's"
            )

    def retrieve_user_id(self):
        data = self.retrieve_user_by_email()
        if data and isinstance(data, list) and len(data) > 0:
            return data[0].get("id")
        return

    def update_employee_level(self):

        if not self.nivel_pdp:
            _logger.error("El nivel del empleado no está definido.")
            raise ValidationError("El nivel del empleado no está definido.")

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        if settings and self.id_crehana:

            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/{self.id_crehana}/custom-fields/"
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            payload = {
                "custom_fields": [
                    {
                        "id": 1944,
                        "value": self.nivel_pdp.upper() if self.nivel_pdp else "",
                        "type": "TEXT",
                    }
                ]
            }

            try:
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()

                _logger.info("Nivel PDP actualizado exitosamente")
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al actualizar nivel PDP: {e}")
                raise ValidationError(f"Error al actualizar nivel PDP: {e}")

    def tyt_crehana_get_employee_level(self):

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        if settings and self.id_crehana:

            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/reports/learning/general/?user_email={self.private_email or self.work_email}"
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()

                _logger.info(f"Datos obtenidos para el reporte del empleado: {data}")

                if data and isinstance(data, list) and len(data) > 0:
                    custom_fields = data[0].get("custom_fields", [])
                    for field in custom_fields:
                        if field.get("id") == 1944:
                            self.nivel_pdp = field.get("value")
                            _logger.info(
                                f"Nivel del empleado actualizado a: {self.nivel_pdp}"
                            )
                            break
                else:
                    _logger.error(
                        f"No se encontró el reporte en Crehana para el email: {self.private_email or self.work_email}"
                    )
                    raise ValidationError(
                        "No se encontró el reporte o el nivel del empleado en Crehana para el email proporcionado."
                    )
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise ValidationError(f"Error al obtener datos: {e}")

    def action_employee_crehana_sync(self):
        # Obtener todos los empleados no registrados en Crehana
        employees = self.search([("is_registered_in_crehana", "=", False)])
        for employee in employees:
            employee.action_register_in_crehana()

    def _parse_date(self, date_str):
        if not date_str or date_str == "None":
            return None
        try:
            return fields.Date.from_string(date_str)
        except:
            return None
        