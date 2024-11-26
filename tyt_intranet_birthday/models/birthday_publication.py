from odoo import api, fields, models, _
from odoo.exceptions import UserError
from random import randint
from datetime import date
import random

SUPPORTED_IMAGE_MIMETYPES = ['image/gif', 'image/jpe', 'image/jpeg', 'image/jpg', 'image/png', 'image/svg+xml']
SUPPORTED_IMAGE_EXTENSIONS = ['.gif', '.jpe', '.jpeg', '.jpg', '.png', '.svg']

class BirthdayDaily(models.Model):
    _name = 'tyt.intranet.birthday_daily'
    _description = 'Birthday Daily'

    birthday_publication_id = fields.Many2one('tyt.intranet.birthday_publication', string='Birthday Publication')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    birthday = fields.Date(relate='employee_id.birthday', string='Birthday')
    birthday_card = fields.Binary(string='Birthday Card')
    birthday_card_filename = fields.Char(string='Birthday Card Filename')


class BirthdayPublication(models.Model):
    _name = 'tyt.intranet.birthday_publication'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Birthday Publication'

    birthday_daily_ids = fields.One2many('tyt.intranet.birthday_daily', 'birthday_publication_id',
                                         string='Birthday Daily')
    employee_ids = fields.Many2many('hr.employee', string='Employees')

    name = fields.Char(string='Title')
    responsible_id = fields.Many2one('res.users', string='Responsible', domain="[('share', '=', False)]",
                                     default=lambda self: self.env.user)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', compute='_compute_attachments', store=False)
    birthday_employee_ids = fields.Many2many('hr.employee', relation='birthday_publication_employee_rel',
                                             column1='publication_id', column2='employee_id', string='Birthday Employees')
    employee_count = fields.Integer(string='Employee Count', compute='_compute_employee_count')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    def _compute_employee_count(self):
        for record in self:
            record.employee_count = self.env['hr.employee'].search_count([])

    def action_show_employees(self):
        self.ensure_one()
        return {
            'name': _('Employees'),
            'view_mode': 'tree,form',
            'res_model': 'hr.employee',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'target': 'current',
        }

    @api.depends('message_attachment_count')
    def _compute_attachments(self):
        for record in self:
            record.attachment_ids = self.env['ir.attachment'].search([
                ('res_model', '=', self._name),
                ('res_id', '=', record.id),
            ])

    @api.model
    def _cron_update_birthday_publication(self):
        employees = self.env['hr.employee'].search([('include_in_birthday_publication', '=', True)])
        employees._compute_is_birthday()
        birthday_employee_ids = employees.filtered(lambda emp: emp.is_birthday)
        birthday_publication_singleton = self.env.ref('tyt_intranet_birthday.tyt_intranet_birthday_publication_singleton',
                                                      raise_if_not_found=False)
        birthday_publication_singleton.write({
            'birthday_employee_ids': [(6, 0, birthday_employee_ids.ids)],
        })
        filtered_attachments = birthday_publication_singleton.attachment_ids.filtered(
            lambda attachment: attachment.mimetype in SUPPORTED_IMAGE_MIMETYPES
        )
        attachment_pool = filtered_attachments.ids and filtered_attachments or None
        for employee in birthday_employee_ids:
            selected_attachment = random.choice(attachment_pool) if attachment_pool else None
            birthday_card_data = selected_attachment.datas if selected_attachment else None
            birthday_card_filename = selected_attachment.name if selected_attachment else None
            employee.write({
                'birthday_card': birthday_card_data,
                'birthday_card_filename': birthday_card_filename,
            })
