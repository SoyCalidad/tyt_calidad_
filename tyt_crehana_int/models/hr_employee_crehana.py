from odoo import api, fields, models
import requests
import logging
from datetime import datetime
import json

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    ENDPOINTS = {
        "GET": {
            "users": "/users",
            "user_detail": "/users/{user_id}",
            "user_courses": "/users/{user_id}/courses",
            "user_progress": "/users/{user_id}/progress",
        },
        "POST": {
            "create_user": "/users",
            "enroll_user": "/users/{user_id}/enroll",
            "update_user": "/users/{user_id}",
            "custom_fields": "/users/{user_id}/custom-fields",
        },
    }

    def _get_crehana_headers(self):
        """Obtiene los headers de autenticación para las peticiones a Crehana API"""
        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()
        return {
            "api-key": settings.api_key,
            "secret-access": settings.secret_access,
            "Content-Type": "application/json",
        }

    def _make_crehana_request(self, method, endpoint, data=None, params=None):
        """Realiza peticiones HTTP a la API de Crehana"""
        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()
        base_url = (
            f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}"
        )
        url = f"{base_url}{endpoint}"
        headers = self._get_crehana_headers()

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method.upper() == "POST":
                _logger.info(f"Esto es un post Data: {data}")
                response = requests.post(
                    url, headers=headers, json=data, params=params, timeout=30
                )
            elif method.upper() == "PUT":
                response = requests.put(
                    url, headers=headers, json=data, params=params, timeout=30
                )
            elif method.upper() == "DELETE":
                response = requests.delete(
                    url, headers=headers, params=params, timeout=30
                )
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")

            response.raise_for_status()
            return response.json() if response.content else {}

        except requests.exceptions.RequestException as e:
            _logger.error(f"Error en petición a Crehana API: {str(e)}")
            raise
        except Exception as e:
            _logger.error(f"Error inesperado en petición a Crehana: {str(e)}")
            raise

    def tyt_get_all_crehana_employees(self):
        """Obtiene todos los usuarios de Crehana de la organización"""
        endpoint = self.ENDPOINTS["GET"]["users"]

        try:
            response = self._make_crehana_request("GET", endpoint)
            _logger.info(
                f"Se obtuvieron {len(response.get('results', []))} usuarios de Crehana"
            )
            return response.get("results", [])
        except Exception as e:
            _logger.error(f"Error al obtener empleados de Crehana: {str(e)}")
            # Crear un mensaje de error chatter
            message = self.env["mail.message"].create(
                {
                    "subject": "Error al obtener empleados de Crehana",
                    "body": f"Error al obtener empleados de Crehana: {str(e)}",
                    "model": "hr.employee",
                    "res_id": self.id,
                }
            )
            return []

    def tyt_get_crehana_employee_by_id(self, user_id):
        """Obtiene un usuario específico de Crehana por su ID"""
        if not user_id:
            _logger.warning("Falta parámetro requerido: user_id")
            return None

        endpoint = self.ENDPOINTS["GET"]["user_detail"].format(user_id=user_id)

        try:
            response = self._make_crehana_request("GET", endpoint)
            _logger.info(f"Usuario {user_id} obtenido exitosamente de Crehana")
            return response
        except Exception as e:
            _logger.error(f"Error al obtener usuario {user_id} de Crehana: {str(e)}")
            return None

    def tyt_get_crehana_employee_courses(self, user_id=None):
        """Obtiene los cursos asignados a un usuario de Crehana"""
        if not user_id and hasattr(self, "id_crehana"):
            user_id = self.id_crehana

        if not user_id:
            _logger.warning("No se proporcionó user_id ni se encontró id_crehana")
            return []

        endpoint = self.ENDPOINTS["GET"]["user_courses"].format(user_id=user_id)

        try:
            response = self._make_crehana_request("GET", endpoint)
            _logger.info(f"Cursos del usuario {user_id} obtenidos exitosamente")
            return response.get("results", [])
        except Exception as e:
            _logger.error(f"Error al obtener cursos del usuario {user_id}: {str(e)}")
            return []

    def tyt_get_crehana_employee_progress(self, user_id=None):
        """Obtiene el progreso de un usuario en sus cursos de Crehana"""
        if not user_id and hasattr(self, "id_crehana"):
            user_id = self.id_crehana

        if not user_id:
            _logger.warning("No se proporcionó user_id ni se encontró id_crehana")
            return {}

        endpoint = self.ENDPOINTS["GET"]["user_progress"].format(user_id=user_id)

        try:
            response = self._make_crehana_request("GET", endpoint)
            _logger.info(f"Progreso del usuario {user_id} obtenido exitosamente")
            return response
        except Exception as e:
            _logger.error(f"Error al obtener progreso del usuario {user_id}: {str(e)}")
            return {}

    def tyt_create_crehana_employee(self, user_data):
        """Crea un nuevo usuario en Crehana"""
        endpoint = self.ENDPOINTS["POST"]["create_user"]

        try:
            response = self._make_crehana_request("POST", endpoint, data=user_data)

            _logger.info(
                f"Usuario creado exitosamente en Crehana: {response.get('id')}"
            )
            return response
        except Exception as e:
            _logger.error(f"Error al crear usuario en Crehana: {str(e)}")
            return None

    def tyt_update_crehana_employee(self, user_data, user_id=None):
        """Actualiza un usuario existente en Crehana"""
        if not user_id and hasattr(self, "id_crehana"):
            user_id = self.id_crehana

        if not user_id:
            _logger.warning("No se proporcionó user_id ni se encontró id_crehana")
            return None

        endpoint = self.ENDPOINTS["POST"]["update_user"].format(user_id=user_id)

        try:
            response = self._make_crehana_request("POST", endpoint, data=user_data)
            _logger.info(f"Usuario {user_id} actualizado exitosamente en Crehana")
            return response
        except Exception as e:
            _logger.error(f"Error al actualizar usuario {user_id} en Crehana: {str(e)}")
            return None

    def tyt_enroll_crehana_employee(self, course_data, user_id=None):
        """Inscribe un usuario en uno o más cursos de Crehana"""
        if not user_id and hasattr(self, "id_crehana"):
            user_id = self.id_crehana

        if not user_id:
            _logger.warning("No se proporcionó user_id ni se encontró id_crehana")
            return None

        endpoint = self.ENDPOINTS["POST"]["enroll_user"].format(user_id=user_id)

        try:
            response = self._make_crehana_request("POST", endpoint, data=course_data)
            _logger.info(f"Usuario {user_id} inscrito exitosamente en cursos")
            return response
        except Exception as e:
            _logger.error(f"Error al inscribir usuario {user_id} en cursos: {str(e)}")
            return None

    def tyt_sync_with_crehana(self):
        """Sincroniza los datos del empleado con Crehana"""
        try:

            if not hasattr(self, "id_crehana") or not self.id_crehana:
                _logger.warning(
                    f"Empleado {self.name} no tiene número de usuario de Crehana configurado"
                )

            # crehana_user = self.retrieve_user_by_email()
            # if crehana_user and not self.id_crehana:
            #     self.id_crehana = crehana_user[0]["id"]

            # else:
            #     _logger.warning(
            #         f"No se encontró usuario en Crehana para empleado {self.name}"
            #     )

            settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()
            if not settings:
                _logger.error("No se encontraron credenciales de Crehana")
                return False
            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/"

            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            if self.crehana_email:
                params = {"search": self.crehana_email}
            else:
                params = {"limit": 10000}

            response = requests.get(url, headers=headers, params=params, timeout=60)
            response.raise_for_status()
            response = response.json()

            crehana_response_data = response["data"]

            if not crehana_response_data:
                crehana_response_data = []

            _logger.info(
                f"Datos de empleados obtenidos de Crehana: {len(crehana_response_data)}"
            )

            crehana_user_data = next(
                (
                    item
                    for item in crehana_response_data
                    if item["id"] == int(self.id_crehana)
                ),
                None,
            )

            if not crehana_user_data:
                _logger.warning(
                    f"No se encontró usuario en Crehana para empleado {self.name}"
                )

            crehana_user = crehana_user_data

            _logger.info(f"Datos del empleado {self.name}: {crehana_user}")

            if crehana_user:
                self.crehana_email = crehana_user.get("email")
                mapping = self._get_custom_fields_mapping()
                for key, meta in mapping.items():
                    cf = next(
                        (
                            x
                            for x in crehana_user.get("custom_fields", [])
                            if isinstance(x, dict) and x.get("id") == key
                        ),
                        None,
                    )
                    if cf:
                        setattr(self, meta["field"], cf.get("value"))

                _logger.info(f"Datos sincronizados para empleado {self.name}")
            else:
                # Mensaje de error en chatter
                message = self.env["mail.message"].create(
                    {
                        "subject": "No se encontró usuario en Crehana",
                        "body": f"No se encontró usuario en Crehana para empleado {self.name}",
                        "model": "hr.employee",
                        "res_id": self.id,
                    }
                )
                _logger.warning(
                    f"No se encontró usuario en Crehana para empleado {self.name}"
                )
        except Exception as e:
            _logger.error(
                f"Error al sincronizar empleado {self.name} con Crehana: {str(e)}"
            )
            # Crear un mensaje de error chatter
            message = self.env["mail.message"].create(
                {
                    "subject": "Error al sincronizar empleado con Crehana",
                    "body": f"Error al sincronizar empleado {self.name} con Crehana: {str(e)}",
                    "res_id": self.id,
                    "res_model": "hr.employee",
                }
            )
            return False

    def action_register_in_crehana(self):
        """Registra el empleado en Crehana y envía campos personalizados"""
        _logger.info("Ejecutando action_register_in_crehana...")

        title = "Datos faltantes"
        message = "Problemas con los datos, contacte con su administrador"

        try:
            # Validar email
            if not self.crehana_email:
                message = "No se encontró email crehana del empleado"
                raise ValueError(message)

            # Procesar nombres del empleado
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
                    raise ValueError(
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

            # Preparar payload para registrar empleado
            payload = {
                "first_name": empleado_nombre,
                "last_name": f"{empleado_paterno} {empleado_materno}",
                "email": self.crehana_email or self.private_email or self.work_email,
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

            # response = self.tyt_create_crehana_employee(payload)
            settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()
            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/"
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            response = response.json()

            _logger.info(f"Respuesta de Crehana: {str(response)}")

            self.id_crehana = response.get("id")
            self.user_crehana = (
                response.get("user").get("username") if response.get("user") else ""
            )
            self.is_registered_in_crehana = True

            title = "Registrado"
            message = "El empleado fue registrado exitosamente"

            _logger.info(f"Empleado registrado exitosamente. ID: {self.id_crehana}")

            self._send_custom_fields_to_crehana()

        except Exception as e:
            _logger.error(f"Error en registro de empleado en Crehana: {str(e)}")
            title = "Error"
            message = f"Error al registrar empleado: {str(e)}"
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": title,
                    "message": message,
                    "type": "danger",
                    "sticky": True,
                },
            }

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

    def action_sync_custom_fields_crehana(self):
        """
        Acción independiente para sincronizar solo los campos personalizados
        """
        return self._send_custom_fields_to_crehana()

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
            return False  # Agregado return False que faltaba

        url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/{self.id_crehana}/custom-fields/"

        headers = {
            "api-key": settings.api_key,
            "secret-access": settings.secret_access,
            "Content-Type": "application/json",
            "Accept": "application/json",  # Agregado para mejor compatibilidad
        }

        payload = self._prepare_custom_fields_payload(field_ids)

        # Asegurar que el payload esté en formato JSON válido con comillas dobles
        try:
            # Convertir a JSON string y luego de vuelta a dict para asegurar formato correcto
            json_string = json.dumps(payload, ensure_ascii=False)
            validated_payload = json.loads(json_string)

            # Log del payload con formato JSON correcto
            _logger.info(f"Enviando campos personalizados a Crehana para {self.name}:")
            _logger.info(f"URL: {url}")
            _logger.info(f"Payload JSON: {json_string}")

        except (TypeError, ValueError) as e:
            _logger.error(f"Error al serializar payload para {self.name}: {str(e)}")
            return False

        try:
            # Usar el payload validado y enviar como JSON
            response = requests.post(
                url,
                json=validated_payload,  # requests.post con json= automáticamente serializa y usa comillas dobles
                headers=headers,
                timeout=30,  # Aumentado timeout para operaciones que podrían ser lentas
            )

            # Log de la respuesta para debugging
            _logger.info(f"Status Code: {response.status_code}")
            _logger.info(f"Response Headers: {dict(response.headers)}")

            # Intentar loggear la respuesta (si es JSON)
            try:
                response_json = response.json()
                _logger.info(
                    f"Response JSON: {json.dumps(response_json, ensure_ascii=False)}"
                )
            except:
                _logger.info(f"Response Text: {response.text}")

            response.raise_for_status()

            _logger.info(
                f"Campos personalizados enviados exitosamente para empleado {self.name}"
            )
            return True

        except requests.exceptions.Timeout:
            _logger.error(f"Timeout al enviar campos personalizados para {self.name}")
            return False

        except requests.exceptions.ConnectionError:
            _logger.error(
                f"Error de conexión al enviar campos personalizados para {self.name}"
            )
            return False

        except requests.exceptions.HTTPError as e:
            # mensaje de error chatter
            message = self.env["mail.message"].create(
                {
                    "subject": "Error al enviar campos personalizados a Crehana",
                    "body": f"Error al enviar campos personalizados a Crehana: {str(e)}",
                    "model": "hr.employee",
                    "res_id": self.id,
                }
            )
            _logger.error(
                f"Error HTTP al enviar campos personalizados para {self.name}: {e}"
            )
            _logger.error(f"Status Code: {response.status_code}")
            _logger.error(f"Response: {response.text}")
            return False

        except Exception as e:
            _logger.error(
                f"Error inesperado al enviar campos personalizados para {self.name}: {str(e)}"
            )
            return False

    # MÉTODO ALTERNATIVO: Si aún tienes problemas, usa este método que serializa manualmente
    def _send_custom_fields_to_crehana_alternative(self, field_ids=None):
        """
        Versión alternativa que serializa manualmente el JSON para garantizar comillas dobles
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
            "Accept": "application/json",
        }

        payload = self._prepare_custom_fields_payload(field_ids)

        try:
            # Serializar manualmente el payload a JSON string
            json_payload = json.dumps(
                payload, ensure_ascii=False, separators=(",", ":")
            )

            _logger.info(f"Enviando campos personalizados a Crehana para {self.name}:")
            _logger.info(f"Payload JSON: {json_payload}")

            # Enviar usando data= en lugar de json= para control total del formato
            response = requests.post(
                url,
                data=json_payload,  # Enviar como string JSON serializado manualmente
                headers=headers,
                timeout=30,
            )

            _logger.info(f"Status Code: {response.status_code}")

            try:
                response_json = response.json()
                _logger.info(
                    f"Response: {json.dumps(response_json, ensure_ascii=False)}"
                )
            except:
                _logger.info(f"Response Text: {response.text}")

            response.raise_for_status()

            _logger.info(
                f"Campos personalizados enviados exitosamente para empleado {self.name}"
            )
            return True

        except Exception as e:
            _logger.error(
                f"Error al enviar campos personalizados para {self.name}: {str(e)}"
            )
            if "response" in locals():
                _logger.error(f"Status Code: {response.status_code}")
                _logger.error(f"Response: {response.text}")
            return False

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
                    try:
                        # Los datos llegan en este formato: %d/%m/%Y debemos formatear a %Y-%m-%d
                        formatted_value = datetime.strptime(
                            field_value, "%d/%m/%Y"
                        ).strftime("%Y-%m-%d")
                    except Exception:
                        formatted_value = field_value
                else:
                    formatted_value = field_value.strftime("%d-%m-%Y")
            elif field_type == "MULTIPLE":
                # Para campos MULTIPLE, enviar como string pero puede contener múltiples valores separados
                formatted_value = str(field_value) if field_value else ""
            else:  # TEXT
                formatted_value = str(field_value) if field_value else ""

            # No añadir si el valor es vacío
            if not formatted_value:
                continue
            custom_fields.append(
                {"id": field_id, "value": formatted_value, "type": field_type}
            )

        return {"custom_fields": custom_fields}

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
            1942: {"field": "x_studio_numero", "type": "TEXT"},
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

    @api.model
    def tyt_sync_all_employees_with_crehana(self):
        """Sincroniza todos los empleados que tienen configurado id_crehana con Crehana"""
        employees_with_crehana = self.search([("id_crehana", "!=", False)])
        results = {"success": 0, "failed": 0, "total": len(employees_with_crehana)}

        for employee in employees_with_crehana:
            if employee.tyt_sync_with_crehana():
                results["success"] += 1
            else:
                results["failed"] += 1

        _logger.info(f"Sincronización masiva completada: {results}")
        return results

    @api.model
    def tyt_sync_from_crehana(self):
        """Obtiene todos los empleados de Crehana y los sincroniza con Odoo"""
        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()
        if not settings:
            _logger.error("No se encontraron credenciales de Crehana")
            return False
        url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/users/"
        headers = {
            "api-key": settings.api_key,
            "secret-access": settings.secret_access,
            "Content-Type": "application/json",
        }
        params = {"limit": 10000}
        response = requests.get(url, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        employees_data = response.json()
        crehana_response_data = employees_data["data"]
        mapping = self._get_custom_fields_mapping()

        for data in crehana_response_data:

            try:

                # Buscar por id
                employee = self.search([("id_crehana", "=", data["id"])])
                # En caso no encontrar, buscamos por apellidos + nombres
                if not employee:
                    employee = self.search(
                        [("name", "=", f"{data['last_name']} {data['first_name']}")]
                    )
                if not employee:
                    _logger.info(
                        f"Empleado no encontrado: {data['first_name']} {data['last_name']}"
                    )
                    # Create message in chatter
                    message = self.env["mail.message"].create(
                        {
                            "subject": f"Empleado no encontrado: {data['first_name']} {data['last_name']}",
                            "body": f"Empleado no encontrado: {data['first_name']} {data['last_name']}",
                            "model": "hr.employee",
                            "res_id": self.id,
                        }
                    )
                    continue

                if employee:
                    _logger.info(
                        f"Sincronizando empleado: {data['first_name']} {data['last_name']}"
                    )
                    employee.write(
                        {
                            "id_crehana": data["id"],
                            "crehana_email": data["email"],
                            "is_registered_in_crehana": True,
                        }
                    )
                    for key, meta in mapping.items():
                        cf = next(
                            (
                                x
                                for x in data.get("custom_fields", [])
                                if isinstance(x, dict) and x.get("id") == key
                            ),
                            None,
                        )
                        if cf:
                            _logger.info(f"Actualizando campo {meta['field']}")
                            setattr(employee, meta["field"], cf.get("value"))

            except Exception as e:
                _logger.error(
                    f"Error al sincronizar empleado: {data['first_name']} {data['last_name']}: {e}"
                )
                # Mensaje en el chatter
                message = self.env["mail.message"].create(
                    {
                        "subject": f"Error al sincronizar empleado: {data['first_name']} {data['last_name']}",
                        "body": f"Error al sincronizar empleado: {data['first_name']} {data['last_name']}: {e}",
                        "model": "hr.employee",
                        "res_id": self.id,
                    }
                )
                continue

        return True
