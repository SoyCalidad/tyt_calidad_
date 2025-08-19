
from odoo import models, fields, api, _
import logging
import requests

_logger = logging.getLogger(__name__)


class TYTCreahanaGeneralReport(models.Model):
    _name = 'tyt.crehana.general.report'
    _description = 'TYT Creahana General Report'

    crehana_user_id = fields.Char(
        string='ID de usuario Crehana',
    )
    crehana_user_name = fields.Char(
        string='Nombre de usuario Crehana',
    )
    crehana_user_email = fields.Char(
        string='Email de usuario Crehana',
    )
    crehana_user_status = fields.Char(
        string='Estado de usuario Crehana',
    )
    crehana_user_info_extra = fields.Char(
        string='Info extra de usuario',
    )
    crehana_is_enroll_active = fields.Boolean(
        string='Inscripción activa',
    )
    creahana_course_id = fields.Char(
        string='ID de curso Crehana',
    )
    creahana_course_name = fields.Char(
        string='Nombre de curso Crehana',
    )
    creahana_course_category = fields.Char(
        string='Categoría de curso Crehana',
    )
    creahana_course_subcategory = fields.Char(
        string='Subcategoría de curso Crehana',
    )
    creahana_is_admin_assigned = fields.Boolean(
        string='Administrador asignado',
    )
    creahana_assigned_by_name = fields.Char(
        string='Asignado por',
    )
    creahana_course_type = fields.Char(
        string='Tipo de curso Crehana',
    )
    creahana_course_is_reward = fields.Char(
        string='Es curso recompensa',
    )
    creahana_course_duration_hours = fields.Float(
        string='Duración del curso (horas)',
    )
    creahana_course_progress = fields.Float(
        string='Progreso del curso (%)',
    )
    creahana_course_progress_hours = fields.Float(
        string='Progreso del curso (horas)',
    )
    creahana_course_is_completed = fields.Boolean(
        string='Curso completado',
    )
    creahana_project_status = fields.Char(
        string='Estado del proyecto',
    )
    creahana_project_date = fields.Date(
        string='Fecha del proyecto',
    )
    creahana_quiz_status = fields.Char(
        string='Estado del quiz',
    )
    creahana_quiz_attempts = fields.Integer(
        string='Intentos de quiz',
    )
    creahana_quiz_best_correct_answers = fields.Integer(
        string='Mejores respuestas correctas',
    )
    creahana_quiz_best_wrong_answers = fields.Integer(
        string='Mejores respuestas incorrectas',
    )
    creahana_quiz_total_questions = fields.Integer(
        string='Total de preguntas del quiz',
    )
    creahana_quiz_best_result = fields.Float(
        string='Mejor resultado del quiz',
    )
    creahana_course_is_certified = fields.Boolean(
        string='Curso certificado',
    )
    creahana_course_has_participation_certificate = fields.Boolean(
        string='Tiene certificado de participación',
    )
    creahana_course_enroll_date = fields.Date(
        string='Fecha de inscripción',
    )
    creahana_course_start_date = fields.Date(
        string='Fecha de inicio',
    )
    creahana_course_complete_date = fields.Date(
        string='Fecha de finalización',
    )
    creahana_project_url = fields.Char(
        string='URL del proyecto',
    )
    creahana_course_certificated_url = fields.Char(
        string='URL del certificado',
    )
    creahana_course_participation_certificate_url = fields.Char(
        string='URL del certificado de participación',
    )
    creahana_course_certificated_date = fields.Date(
        string='Fecha de certificación',
    )
    creahana_course_last_action_date = fields.Date(
        string='Fecha de última acción',
    )
    creahana_user_division = fields.Char(
        string='División del usuario',
    )
    creahana_user_subsidiary = fields.Char(
        string='Subsidiaria del usuario',
    )
    creahana_user_job = fields.Char(
        string='Trabajo del usuario',
    )
    creahana_user_level = fields.Char(
        string='Nivel del usuario',
    )
    creahana_user_role = fields.Char(
        string='Rol del usuario',
    )
    creahana_track_id = fields.Char(
        string='ID del track',
    )
    creahana_track_name = fields.Char(
        string='Nombre del track',
    )
    creahana_track_is_hidden = fields.Boolean(
        string='Track oculto',
    )
    creahana_user_custom_fields = fields.Text(
        string='Campos personalizados',
    )
