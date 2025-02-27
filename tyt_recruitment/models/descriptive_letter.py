# -*- coding: utf-8 -*-

from odoo import api, models, fields, http
from odoo.http import request
import uuid
from io import BytesIO
import base64
from datetime import datetime
from urllib.parse import quote

import logging
_logger = logging.getLogger(__name__)

class DescriptiveLetter(models.Model):
    _name = 'tyt_recruitment.descriptive_letter'
    _description = 'Plantilla de carta descriptiva'
    _rec_name = 'course_name'

    course_name = fields.Char(string="Nombre del curso", required=True)  
    training_location = fields.Char(string="Lugar de instrucción")  
    instructor_name = fields.Char(string="Nombre del instructor")  
    general_objective = fields.Char(string="Objetivo general")  
    participant_profile = fields.Char(string="Perfil de los participantes")  
    entry_knowledge_and_skills = fields.Char(string="Conocimiento y habilidades para ingresar al curso")  

    site = fields.Many2one('x_sitios', string="Sitio", required=True)

    day_ids = fields.One2many('tyt_recruitment.descriptive_letter_day', 'descriptive_letter_id', string="Días")
    framing_topic_ids = fields.One2many('tyt_recruitment.descriptive_letter_framing_topic', 'descriptive_letter_id', string="Encuadre - temas")

    def copy(self, default=None):
        default = default or {}

        # Cambiar el nombre para evitar duplicados con el mismo nombre
        default['course_name'] = f"{self.course_name} (copia)"

        # Duplicar los días relacionados (day_ids)
        default['day_ids'] = [(0, 0, {
            'name': day.name,  
            # Agrega otros campos de 'tyt_recruitment.descriptive_letter_day' si es necesario
        }) for day in self.day_ids]

        # Duplicar los temas de encuadre (framing_topic_ids) con sus subtemas
        default['framing_topic_ids'] = [(0, 0, {
            'name': topic.name,
            'descriptive_letter_id': False,  # Evita relación con la carta original
            'framing_subtopic_ids': [(0, 0, {
                'name': subtopic.name,
                'instructor_learning_activities': subtopic.instructor_learning_activities,
                'participant_learning_activities': subtopic.participant_learning_activities,
                'instructional_techniques': subtopic.instructional_techniques,
                'group_techniques': subtopic.group_techniques,
                'evaluation': subtopic.evaluation,
                'required_material': subtopic.required_material,
                'time': subtopic.time,
            }) for subtopic in topic.framing_subtopic_ids]
        }) for topic in self.framing_topic_ids]

        return super(DescriptiveLetter, self).copy(default)

    def action_view_descriptive_letter_form(self):

        url = f"/descriptive_letter/template/{self.id}/0"

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new', 
        }

# Temas de encuadre en carta descriptiva

class FramingTopic(models.Model):
    _name = 'tyt_recruitment.descriptive_letter_framing_topic'
    _description = 'Tema de encuadre en plantilla de carta descriptiva'
    _rec_name = 'id'

    name = fields.Char(string="Objetivo particular/Específico")

    descriptive_letter_id = fields.Many2one("tyt_recruitment.descriptive_letter", string="Plantilla de carta descriptiva")
    descriptive_letter_input_id = fields.Many2one("tyt_recruitment.descriptive_letter_input", string="Plantilla de carta descriptiva")

    framing_subtopic_ids = fields.One2many('tyt_recruitment.descriptive_letter_framing_subtopic', 'framing_topic_id', string="Subtemas")

class FramingSubtopic(models.Model):
    _name = 'tyt_recruitment.descriptive_letter_framing_subtopic'
    _description = 'Subtema de encuedre en plantilla de carta descriptiva'
    _rec_name = 'id'

    name = fields.Char(string="Nombre del Subtema")
    instructor_learning_activities = fields.Text(string="INSTRUCTOR - ACTIVIDADES DE APRENDIZAJE")  
    participant_learning_activities = fields.Text(string="PARTICIPANTE - ACTIVIDADES DE APRENDIZAJE")  
    instructional_techniques = fields.Char(string="Técnicas instruccionales")  
    group_techniques = fields.Char(string="Técnicas grupales")  
    evaluation = fields.Char(string="Evaluación")  
    required_material = fields.Char(string="Material requerido")  
    time = fields.Char(string="Tiempo")  

    framing_topic_id = fields.Many2one("tyt_recruitment.descriptive_letter_framing_topic", string="Tema")

# Días en carta descriptiva

class Day(models.Model):
    _name = 'tyt_recruitment.descriptive_letter_day'
    _description = 'Día de Plantilla de carta descriptiva'
    _rec_name = 'id'

    name = fields.Char(string="Nombre")

    descriptive_letter_id = fields.Many2one("tyt_recruitment.descriptive_letter", string="Promedio de Evaluación")
    descriptive_letter_input_id = fields.Many2one("tyt_recruitment.descriptive_letter_input", string="Plantilla de carta descriptiva")

    topic_ids = fields.One2many('tyt_recruitment.descriptive_letter_topic', 'day_id', string="Temas")

class Topic(models.Model):
    _name = 'tyt_recruitment.descriptive_letter_topic'
    _description = 'Tema de Plantilla de carta descriptiva'
    _rec_name = 'id'

    name = fields.Char(string="Objetivo particular/Específico")
    day_id = fields.Many2one("tyt_recruitment.descriptive_letter_day", string="Promedio de Evaluación")

    subtopic_ids = fields.One2many('tyt_recruitment.descriptive_letter_subtopic', 'topic_id', string="Subtemas")

class Subtopic(models.Model):
    _name = 'tyt_recruitment.descriptive_letter_subtopic'
    _description = 'SubtemaPlantilla de carta descriptiva'
    _rec_name = 'id'

    name = fields.Char(string="Nombre del subtema")
    instructor_learning_activities = fields.Text(string="INSTRUCTOR - ACTIVIDADES DE APRENDIZAJE")  
    participant_learning_activities = fields.Text(string="PARTICIPANTE - ACTIVIDADES DE APRENDIZAJE")  
    instructional_techniques = fields.Char(string="Técnicas instruccionales")  
    group_techniques = fields.Char(string="Técnicas grupales")  
    evaluation = fields.Char(string="Evaluación")  
    required_material = fields.Char(string="Material requerido")  
    time = fields.Char(string="Tiempo")  

    topic_id = fields.Many2one("tyt_recruitment.descriptive_letter_topic", string="Promedio de Evaluación")

# Ingreso de carta descriptiva

class DescriptiveLetterInput(models.Model):
    _name = 'tyt_recruitment.descriptive_letter_input'
    _description = 'Carta descriptiva ingresada'
    _rec_name = 'id'

    name = fields.Char(string="Nombre", required=True)
    site = fields.Many2one('x_sitios', string="Sitio", required=True)
    template = fields.Many2one('tyt_recruitment.descriptive_letter', string="Plantilla")

    framing_topic_ids = fields.One2many('tyt_recruitment.descriptive_letter_framing_topic', 'descriptive_letter_input_id', string="Encuadre - temas")
    day_ids = fields.One2many('tyt_recruitment.descriptive_letter_day', 'descriptive_letter_input_id', string="Días")

    @api.onchange('site')
    def _onchange_site(self):
        if self.site:
            return {'domain': {'template': [('site', '=', self.site.id)]}}
        return {'domain': {'template': []}}

    def action_view_descriptive_letter_input_form(self):

        url = f"/descriptive_letter/descriptive_letter/{self.template.id}/{self.id}"

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new', 
        }