from odoo import api, fields, models, _
from odoo.exceptions import UserError
from random import randint
from datetime import date
import random

SUPPORTED_IMAGE_MIMETYPES = ['image/gif', 'image/jpe', 'image/jpeg', 'image/jpg', 'image/png', 'image/svg+xml']


class BirthdayPublication(models.Model):
    _name = 'tyt.intranet.birthday_publication'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Birthday Publication'

    name = fields.Char(string='Title', tracking=True)
    responsible_id = fields.Many2one('res.users', string='Responsible', domain="[('share', '=', False)]",
                                     default=lambda self: self.env.user, tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', compute='_compute_attachments', store=False)
    birthday_employee_ids = fields.Many2many('hr.employee', relation='birthday_publication_employee_rel',
                                             column1='publication_id', column2='employee_id', string='Birthday Employees')
    employee_count = fields.Integer(string='Employee Count', compute='_compute_employee_count')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    def _compute_employee_count(self):
        for record in self:
            record.employee_count = self.env['hr.employee'].search_count([])

    @api.depends('message_attachment_count')
    def _compute_attachments(self):
        for record in self:
            attachments = self.env['ir.attachment'].search([
                ('res_model', '=', self._name),
                ('res_id', '=', record.id),
            ])
            filtered_attachments = attachments.filtered(
                lambda attachment: attachment.mimetype in SUPPORTED_IMAGE_MIMETYPES
            )
            record.attachment_ids = filtered_attachments

    @api.model
    def _cron_update_birthday_publication(self):
        birthday_publication_singleton = self.env.ref(
            'tyt_intranet_birthday.tyt_intranet_birthday_publication_singleton', raise_if_not_found=False)
        attachment_pool = birthday_publication_singleton.attachment_ids

        Employee = self.env['hr.employee']
        Employee._cron_update_birthday_status()
        employees = self.env['hr.employee'].search([('include_in_birthday_publication', '=', True), ('is_birthday', '=', True)])
        birthday_publication_singleton.write({
            'birthday_employee_ids': [(6, 0, employees.ids)],
        })

        no_custom_card_employees = employees.filtered(lambda employee: not employee.has_uploaded_custom_card)
        for employee in no_custom_card_employees:
            selected_attachment = random.choice(attachment_pool) if attachment_pool else None
            birthday_card_data = selected_attachment.datas if selected_attachment else None
            birthday_card_filename = selected_attachment.name if selected_attachment else None
            employee.write({
                'birthday_card': birthday_card_data,
                'birthday_card_filename': birthday_card_filename,
            })
