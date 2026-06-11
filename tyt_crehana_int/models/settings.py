# -*- coding: utf-8 -*-
import requests
from odoo import models, fields, api, _

from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)


class MyModuleSettings(models.Model):
    _name = "tyt_crehana.crehana_settings"
    _description = "Configuraciones"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "organization_slug"

    api_key = fields.Char(string="api-Key")
    secret_access = fields.Char(string="secret-access")
    organization_slug = fields.Char(string="Organización", tracking=True)

    @api.model
    def get_first_settings(self):
        return self.search([], limit=1)

    def write(self, vals):
        for record in self:
            if "api_key" in vals:
                record.message_post(
                    body=_("La API_KEY ha sido actualizada."),
                    subtype_xmlid="mail.mt_note",
                )
            if "secret_access" in vals:
                record.message_post(
                    body=_("El SECRET_ACCESS ha sido actualizado."),
                    subtype_xmlid="mail.mt_note",
                )
        return super(MyModuleSettings, self).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        _logger.info("call create crehana_settings")
        # Verificar si ya existe un registro
        if self.search([]):
            raise UserError(
                "Ya existe un registro de configuración. No puedes crear otro."
            )
        return super(MyModuleSettings, self).create(vals_list)

    def action_view_general_progress_report(self):
        _logger.info("call action_view_general_progress_report")

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        if settings:

            url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/reports/learning/general/"

            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()

                data = response.json()

                if "results" not in data:
                    return {
                        "type": "ir.actions.client",
                        "tag": "display_notification",
                        "params": {
                            "title": "No se obtuvo datos",
                            "message": "La respuesta no contiene los resultados esperados",
                            "type": "success",
                            "sticky": False,
                        },
                    }
                else:
                    self.env["tyt_crehana.user_progress"].search([]).unlink()

                    for item in data.get("results", []):
                        self.env["tyt_crehana.user_progress"].create(
                            {
                                "user_id": item.get("user_id", ""),
                                "user_name": item.get("user_name", ""),
                                "user_email": item.get("user_email", ""),
                                "user_status": item.get("user_status", ""),
                                "user_info_extra": item.get("user_info_extra", ""),
                                "is_enroll_active": item.get("is_enroll_active", ""),
                                "course_id": item.get("course_id", ""),
                                "course_name": item.get("course_name", ""),
                                "course_category": item.get("course_category", ""),
                                "course_subcategory": item.get(
                                    "course_subcategory", ""
                                ),
                                "is_admin_assigned": item.get("is_admin_assigned", ""),
                                "assigned_by_name": item.get("assigned_by_name", ""),
                                "course_type": item.get("course_type", ""),
                                "course_is_reward": item.get("course_is_reward", ""),
                                "course_duration_hours": item.get(
                                    "course_duration_hours", ""
                                ),
                                "course_progress": item.get("course_progress", ""),
                                "course_progress_hours": item.get(
                                    "course_progress_hours", ""
                                ),
                                "course_is_completed": item.get(
                                    "course_is_completed", ""
                                ),
                                "project_status": item.get("project_status", ""),
                                "project_date": item.get("project_date", ""),
                                "quiz_status": item.get("quiz_status", ""),
                                "quiz_attemps": item.get("quiz_attemps", ""),
                                "quiz_best_correct_answers": item.get(
                                    "quiz_best_correct_answers", ""
                                ),
                                "quiz_best_wrong_answers": item.get(
                                    "quiz_best_wrong_answers", ""
                                ),
                                "quiz_total_questions": item.get(
                                    "quiz_total_questions", ""
                                ),
                                "quiz_best_result": item.get("quiz_best_result", ""),
                                "course_is_certified": item.get(
                                    "course_is_certified", ""
                                ),
                                "course_has_participation_certificate": item.get(
                                    "course_has_participation_certificate", ""
                                ),
                                "course_enroll_date": item.get(
                                    "course_enroll_date", ""
                                ),
                                "course_start_date": item.get("course_start_date", ""),
                                "course_complete_date": item.get(
                                    "course_complete_date", ""
                                ),
                                "project_url": item.get("project_url", ""),
                                "course_certificated_url": item.get(
                                    "course_certificated_url", ""
                                ),
                                "course_participation_certificate_url": item.get(
                                    "course_participation_certificate_url", ""
                                ),
                                "course_certificated_date": item.get(
                                    "course_certificated_date", ""
                                ),
                                "course_last_action_date": item.get(
                                    "course_last_action_date", ""
                                ),
                                "user_division": item.get("user_division", ""),
                                "user_subsidiary": item.get("user_subsidiary", ""),
                                "user_job": item.get("user_job", ""),
                                "user_level": item.get("user_level", ""),
                                "user_role": item.get("user_role", ""),
                                "track_id": item.get("track_id", ""),
                                "track_name": item.get("track_name", ""),
                                "track_is_hidden": item.get("track_is_hidden", ""),
                                "user_custom_fields": item.get(
                                    "user_custom_fields", ""
                                ),
                            }
                        )

                return {
                    "type": "ir.actions.act_window",
                    "name": "Reporte de avances",
                    "res_model": "tyt_crehana.user_progress",
                    "view_mode": "list",
                    "res_id": self.id,
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

    def action_fetch_paths_from_api(self):
        _logger.info("call action_fetch_paths_from_api")
        self.fetch_paths_from_api()
        return {
            "name": "Lista de rutas de aprendizaje",
            "type": "ir.actions.act_window",
            "res_model": "tyt_crehana.learning_path",
            "view_mode": "list",
            "view_id": self.env.ref(
                "tyt_crehana_int.tyt_crehana_learning_path_tree_view"
            ).id,
            "target": "current",
        }

    @api.model
    def fetch_paths_from_api(self):
        _logger.info("Ejecutando fetch_paths_from_api...")

        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        if settings:

            url = f"https://www.crehana.com/api/rest/org/{settings.organization_slug}/"
            headers = {
                "api-key": settings.api_key,
                "secret-access": settings.secret_access,
                "Content-Type": "application/json",
            }

            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()

                for item in data.get("tracks", []):

                    id_path = item.get("id")
                    if not id_path:
                        continue

                    path = self.env["tyt_crehana.learning_path"].search(
                        [("id_path", "=", id_path)], limit=1
                    )

                    if not path:
                        new_data = {
                            "id_path": id_path,
                            "name": item.get("name", "Sin Nombre"),
                        }
                        path = self.env["tyt_crehana.learning_path"].create(new_data)

                    existing_course_ids = path.course_ids.mapped("id_course")
                    courses_to_create = []

                    for course in item.get("courses", []):

                        course_id = course.get("id")
                        if not course_id:
                            continue

                        if course_id not in existing_course_ids:
                            new_data_course = {
                                "id_course": course_id,
                                "title": course.get("title", "Sin Nombre"),
                                "path_id": path.id,
                            }
                            courses_to_create.append(new_data_course)
                    if courses_to_create:
                        self.env["tyt_crehana.learning_path_course"].create(
                            courses_to_create
                        )

            except requests.exceptions.RequestException as e:
                _logger.error(f"Error al obtener datos: {e}")
                raise ValidationError(f"Error al obtener datos: {e}")
        else:
            _logger.error(f"Error de credenciales de acceso")
            raise ValidationError(
                "Error al obtener credenciales de acceso para API's"
            )

        return True

    def _parse_date(self, date_str):
        if not date_str or date_str == "None":
            return None
        try:
            return fields.Date.from_string(date_str)
        except:
            return None

    def tyt_sync_from_crehana(self):
        """Obtiene todos los empleados de Crehana y los sincroniza con Odoo"""
        HrEmployee = self.env["hr.employee"]
        HrEmployee.tyt_sync_from_crehana()

    def action_show_general_report(self):
        settings = self.env["tyt_crehana.crehana_settings"].get_first_settings()

        url = f"https://www.crehana.com/api/v5/rest/org/{settings.organization_slug}/reports/learning/general/"
        headers = {
            "api-key": settings.api_key,
            "secret-access": settings.secret_access,
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            existing_records = self.env["tyt.crehana.general.report"].search([])
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
                _logger.info(f"Se crearon {len(records_to_create)} nuevos registros")

            if records_to_update:
                for record, data in records_to_update:
                    record.write(data)
                _logger.info(
                    f"Se actualizaron {len(records_to_update)} registros existentes"
                )

            return {
                "type": "ir.actions.act_window",
                "name": "Reporte General",
                "res_model": "tyt.crehana.general.report",
                "view_mode": "list",
            }
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error al obtener datos: {e}")
            raise ValidationError(f"Error al obtener datos: {e}")


class ItemProgress(models.TransientModel):
    _name = "tyt_crehana.user_progress"
    _description = "Reporte de progreso"
    _rec_name = "user_name"

    user_id = fields.Char(string="user_id")
    user_name = fields.Char(string="user_name")
    user_email = fields.Char(string="user_email")
    user_status = fields.Char(string="user_status")
    user_info_extra = fields.Char(string="user_info_extra")
    is_enroll_active = fields.Char(string="is_enroll_active")
    course_id = fields.Char(string="course_id")
    course_name = fields.Char(string="course_name")
    course_category = fields.Char(string="course_category")
    course_subcategory = fields.Char(string="course_subcategory")
    is_admin_assigned = fields.Char(string="is_admin_assigned")
    assigned_by_name = fields.Char(string="assigned_by_name")
    course_type = fields.Char(string="course_type")
    course_is_reward = fields.Char(string="course_is_reward")
    course_duration_hours = fields.Char(string="course_duration_hours")
    course_progress = fields.Char(string="course_progress")
    course_progress_hours = fields.Char(string="course_progress_hours")
    course_is_completed = fields.Char(string="course_is_completed")
    project_status = fields.Char(string="project_status")
    project_date = fields.Char(string="project_date")
    quiz_status = fields.Char(string="quiz_status")
    quiz_attemps = fields.Char(string="quiz_attemps")
    quiz_best_correct_answers = fields.Char(string="quiz_best_correct_answers")
    quiz_best_wrong_answers = fields.Char(string="quiz_best_wrong_answers")
    quiz_total_questions = fields.Char(string="quiz_total_questions")
    quiz_best_result = fields.Char(string="quiz_best_result")
    course_is_certified = fields.Char(string="course_is_certified")
    course_has_participation_certificate = fields.Char(
        string="course_has_participation_certificate"
    )
    course_enroll_date = fields.Char(string="course_enroll_date")
    course_start_date = fields.Char(string="course_start_date")
    course_complete_date = fields.Char(string="course_complete_date")
    project_url = fields.Char(string="project_url")
    course_certificated_url = fields.Char(string="course_certificated_url")
    course_participation_certificate_url = fields.Char(
        string="course_participation_certificate_url"
    )
    course_certificated_date = fields.Char(string="course_certificated_date")
    course_last_action_date = fields.Char(string="course_last_action_date")
    user_division = fields.Char(string="user_division")
    user_subsidiary = fields.Char(string="user_subsidiary")
    user_job = fields.Char(string="user_job")
    user_level = fields.Char(string="user_level")
    user_role = fields.Char(string="user_role")
    track_id = fields.Char(string="track_id")
    track_name = fields.Char(string="track_name")
    track_is_hidden = fields.Char(string="track_is_hidden")
    user_custom_fields = fields.Char(string="user_custom_fields")
