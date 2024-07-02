# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Employee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee', 'mgmtsystem.code']

    trainings_count = fields.Integer(
        string=u'Capacitaciones',
        compute='_compute_trainings_count',
        store=False,
    )

    training_line_ids = fields.One2many(
        string=u'training_line',
        comodel_name='mgmtsystem.plan.training.line',
        inverse_name='employee_id',
    )

    new_user_id = fields.Many2one('hr.employee', string='Contacto')

    job_title = fields.Char(related='job_id.name', string='Cargo')
    job_name = fields.Char(related='job_id.name', string='Cargo')

    @api.onchange('address_home_id')
    def _onchange_new_user_id(self):
        self.identification_id = self.address_home_id.vat

    @api.depends('training_line_ids')
    def _compute_trainings_count(self):
        for record in self:
            record.trainings_count = len(record.training_line_ids) or 0

    type_blood = fields.Selection([
        ('1', 'A Positiva'),
        ('2', 'A Negativa'),
        ('3', 'B Positiva'),
        ('4', 'B Negativa'),
        ('5', 'O Positiva'),
        ('4', 'O Negativa'),
        ('6', 'AB Positiva'),
        ('7', 'AB Negativa'),
    ],
        string=u'Tipo de sangre',
    )
    license_driver = fields.Char(
        string=u'Licencia de conducir',
    )
    category_driver = fields.Selection([
        ('1', ' Clase A-I'),
        ('2', ' Clase A-IIa'),
        ('3', ' Clase A-IIb'),
        ('4', ' Clase A-IIIa'),
        ('5', ' Clase A-IIIb'),
        ('4', ' Clase A-IIIc'),
        ('6', ' B-I'),
        ('7', ' B-IIa'),
        ('8', ' B-IIb'),
        ('9', ' B-IIc'),
    ],
        string=u'Categoría',
    )
    level = fields.Char(
        string=u'Nivel',
    )
    institution = fields.Char(
        string=u'Institución',
    )
    profession = fields.Char(
        string=u'Profesión',
    )
    obtained_title = fields.Char(
        string=u'Título obtenido',
    )
    school = fields.Char(
        string=u'Colegio Nº',
    )
    enabled = fields.Char(
        string=u'Habilitado',
    )
    language = fields.Char(
        string=u'Idioma',
    )
    other_languages = fields.Text(string='Otros idiomas')

    # Muliple jobs

    multiple_job_ids = fields.Many2many('hr.job', string='Puestos de trabajo')
    multiple_department_ids = fields.Many2many(
        'hr.department', string='Departamentos')

    # RUC data

    document_type_id = fields.Many2one(
        'hr.employee.document_type', string='Tipo de documento')


class HrEmployeeDocumentType(models.Model):
    _name = 'hr.employee.document_type'
    _description = 'Hr Employee Document Type'

    name = fields.Char('Documento', required=True)
