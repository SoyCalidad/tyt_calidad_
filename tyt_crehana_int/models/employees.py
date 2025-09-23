# -*- coding: utf-8 -*-
import requests
from odoo import api, models, fields

import xlsxwriter
from io import BytesIO

import logging

_logger = logging.getLogger(__name__)


class EmployeeExtension(models.Model):
    _inherit = "hr.employee"

    id_crehana = fields.Char(string="Identificacdor Crehana")
    user_crehana = fields.Char(string="Username")
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
    def search(self, args, offset=0, limit=None, order=None, count=False):
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
            args, offset=offset, limit=limit, order=order, count=count
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
                    raise models.ValidationError(
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
                raise models.ValidationError(f"Error al obtener datos: {e}")

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
            raise models.ValidationError(
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

            email = self.private_email or self.work_email

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
                    raise models.ValidationError(
                        "No se encontró el usuario en Crehana para el email proporcionado."
                    )
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
                    "Content-Type": "application/x-www-form-urlencoded",
                }

                # Obtener ruta para su posición
                position = (
                    self.env["tyt_crehana.job_positions"]
                    .sudo()
                    .search([("job_id", "=", self.job_id.id)])
                )

                path_selected = None
                if position.level_a and self.level == "A":
                    path_selected = position.path_to_position_a
                elif position.level_b and self.level == "B":
                    path_selected = position.path_to_position_b
                elif position.level_c and self.level == "C":
                    path_selected = position.path_to_position_c
                elif position.level_d and self.level == "D":
                    path_selected = position.path_to_position_d

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
                        raise models.ValidationError(f"Error al obtener datos: {e}")
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
            raise models.ValidationError(
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
                        new_data["level_of_employee"] = self.level
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
                raise models.ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise models.ValidationError(
                "Error al obtener credenciales de acceso para API's"
            )

    def action_show_user_report(self):

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        if settings:

            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/reports/learning/general/?user_email={self.private_email or self.work_email}"

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                data = response.json()

                _logger.info(f"Datos obtenidos para el reporte del empleado: {data}")

                email = self.private_email or self.work_email

                return {
                    "type": "ir.actions.act_window",
                    "name": "Reporte del Empleado",
                    "res_model": "tyt.crehana.general.report",
                    "view_mode": "tree",
                    "res_id": False,
                    "domain": [("crehana_user_email", "=", email)],
                    "target": "current",
                }
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise models.ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise models.ValidationError(
                "Error al obtener credenciales de acceso para API's"
            )

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
                raise models.ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise models.ValidationError(
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
                raise models.ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise models.ValidationError(
                "Error al obtener credenciales de acceso para API's")

    def retrieve_user_id(self):
        data = self.retrieve_user_by_email()
        if data and isinstance(data, list) and len(data) > 0:
            return data[0].get("id")
        return
        
    def update_employee_level(self):

        if not self.level:
            _logger.error("El nivel del empleado no está definido.")
            raise models.ValidationError("El nivel del empleado no está definido.")

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
                    {"id": 1944, "value": self.level or "", "type": "TEXT"}
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
                            self.level = field.get("value")
                            _logger.info(
                                f"Nivel del empleado actualizado a: {self.level}"
                            )
                            break
                else:
                    _logger.error(
                        f"No se encontró el reporte en Crehana para el email: {self.private_email or self.work_email}"
                    )
                    raise models.ValidationError(
                        "No se encontró el reporte o el nivel del empleado en Crehana para el email proporcionado."
                    )
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise models.ValidationError(f"Error al obtener datos: {e}")

    def action_employee_crehana_sync(self):
        # Obtener todos los empleados no registrados en Crehana
        employees = self.search([("is_registered_in_crehana", "=", False)])
        for employee in employees:
            employee.action_register_in_crehana()
