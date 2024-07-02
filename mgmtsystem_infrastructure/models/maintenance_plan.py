# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

from datetime import tzinfo, date, datetime, timedelta
import pandas as pd

class Frequency(models.Model):
    _name = 'mgmtsystem.maintenance.frequency'
    _description = "Frecuencia de mantenimiento de plan"

    name = fields.Char(
        string='Nombre',
        required=True
    )
    number = fields.Integer(
        string='Cantidad',
        index=True,
        default=15,
        help="Numero de veces que se va a repetir"
    )
    type = fields.Selection(
        string='Periodo',
        selection=[('day', 'Días'), ('week', 'Semana')],
        default='day',
    )


class MaintenancePlan(models.Model):
    _name = 'mgmtsystem.maintenance.plan'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = "Programa de mantenimientos"

    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.maintenance.plan', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.maintenance.plan', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_infrastructure.mgmtsystem_maintenance_plan_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    name = fields.Char(
        string=u'Nombre',
        required=True,
        default="Programa de Mantenimientos"
    )

    numero = fields.Char(
        string="Numero de secuencia",
        readonly=True,
        required=True,
        copy=False,
        default='Sin definir'
    )

    def _default_edition(self):
        process = self.env['res.company'].browse(
            self.env.user.company_id.id).maintenance_process_id
        if process:
            edition = self.env['process.edition'].search([
                ('process_id', '=', process.id),
                ('state', '=', 'validate_ok'),
                ('active', '=', True)
            ], order='create_date desc', limit=1)
            return edition
        else:
            return

    edition_id = fields.Many2one(
        string=u'Procedimiento',
        comodel_name='process.edition',
        domain="[('state', '=', 'validate_ok'), ('active', '=', True)]",
        ondelete='cascade',
        default=_default_edition,
    )

    maintenance_ids = fields.One2many(
        string='Mantenimientos',
        comodel_name='mgmtsystem.maintenance',
        inverse_name='plan_id',
        copy=True,
    )
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.maintenance.plan', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.maintenance.plan', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    maintenances_count = fields.Integer(
        string='Mantenimientos', compute='_get_maintenances_count')

    def _get_maintenances_count(self):
        for each in self:
            if each.maintenance_ids:
                each.maintenances_count = len(each.maintenance_ids)
            else:
                each.maintenances_count = 0

    def open_maintenance_ids(self):
        for each in self:
            ids = [x.id for x in each.maintenance_ids]
            result = self.env.ref(
                'mgmtsystem_infrastructure.mgmtsystem_maintenance_action').read()[0]
            result['domain'] = [('id', 'in', ids)]
            return result

    def create_action(self, vuser_id):
        action = self.env.ref('hola_calidad.p_mail_activity_action').read()[0]
        self.env.cr.execute("""SELECT id FROM ir_model 
        WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
            action['context'] = {
                'default_res_id': self.ids[0],
                'default_res_model': self._name,
                'default_res_model_id': model_id,
                'default_user_id': vuser_id,
            }
        return action

    def action_reset_all_aproval(self):
        for line in self.maintenance_ids:
            line.aproval = True


class Maintenance(models.Model):
    _name = 'mgmtsystem.maintenance'
    _inherit = 'mgmtsystem.validation.mail'
    _description = "Plan de mantenimiento"

    name = fields.Char(u'Nombre del plan', required=True)

    plan_id = fields.Many2one(
        string='Programa origen',
        comodel_name='mgmtsystem.maintenance.plan',
        ondelete='cascade',
    )

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('in_process', 'En proceso'),
            ('final', 'Finalizado'),
            ('caducated', 'Caducado'),
            ('cancel', 'Obsoleto')
        ],
        default='elaborate',
        copy=False,
    )

    employee_id = fields.Many2one(
        string=u'Responsable',
        comodel_name='hr.employee',
        ondelete='cascade',
        required=True,
    )
    responsable_id = fields.Many2one(
        comodel_name='res.users', string='Creado por', required=True)

    type = fields.Selection(
        string=u'Tipo',
        selection=[('interna', 'Interna'), ('externa', 'Externa')],
    )
    start_date = fields.Date(
        string=u'Fecha inicio',
        required=True,
    )
    limit_date = fields.Date(
        string=u'Fecha fin',
        required=True,
    )
    estimate = fields.Float(compute='_get_estimate',
                            string=u'Presupuesto total')

    frequency_id = fields.Many2one(
        string=u'Frecuencia',
        comodel_name='mgmtsystem.maintenance.frequency',
        copy=True,
    )
    new_frequency_id = fields.Many2one(
        string='Frecuencia',
        comodel_name='mgmtsystem.frequency',
        required=True,
    )

    aproval = fields.Boolean(u'Aprobada')

    equipment_ids = fields.Many2many(
        string='Equipos',
        comodel_name='maintenance.equipment',
        relation='mgmtsystem_maintenance_equipment',
        column1='equipment_id',
        column2='maintenance_id',
    )
    line_ids = fields.One2many(
        string='Lineas',
        comodel_name='mgmtsystem.maintenance.line',
        inverse_name='maintenance_id',
    )

    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.maintenance', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.maintenance', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    request_count = fields.Integer(
        compute='_compute_request_count', string='Acciones')

    def write(self, vals):
        confirm = True if self.line_ids else False
        for line in self.line_ids:
            for request in line.maintenance_request_ids:
                if request.state not in ('4repaired', '5scrap'):
                    confirm = False
                    break
        if confirm:
            vals['state'] = 'final'
        return super().write(vals)

    def _compute_request_count(self):
        for each in self:
            total = 0
            if each.line_ids:
                for req in each.line_ids:
                    total += len(req.maintenance_request_ids)
            each.request_count = total

    def show_request_maintenance_action(self):
        ids = []
        for each in self:
            for req in each.line_ids:
                ids.extend(req.maintenance_request_ids.ids)
        result = self.env.ref(
            'maintenance.hr_equipment_request_action').read()[0]
        result['domain'] = [('id', 'in', ids)]
        return result

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_infrastructure.mgmtsystem_maintenance_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    @api.depends('line_ids')
    def _get_estimate(self):
        for each in self:
            amount = 0.0
            for line in each.line_ids:
                for req in line.maintenance_request_ids:
                    amount += req.cost
            each.estimate = amount

    def _get_next_date(self, next_date):
        if self.frequency_id.type == 'day':
            next_date = next_date + timedelta(days=self.frequency_id.number)
            weekday = next_date.weekday()
        if self.frequency_id.type == 'week':
            next_date = next_date + timedelta(weeks=self.frequency_id.number)
            weekday = next_date.weekday()
        if weekday == 5:
            next_date += timedelta(days=2)
        elif weekday == 6:
            next_date += timedelta(days=1)

        return next_date

    def create_cronograma(self):
        for record in self:
            start_date = record.start_date
            limit_date = record.limit_date
            next_date = record._get_next_date(start_date)
            new_ids = []
            while next_date < limit_date:
                new_line = self.env['mgmtsystem.maintenance.line'].create({
                    'maintenance_id': record.id,
                    'name': record.name + " " + next_date.strftime('%d/%m/%Y'),
                })
                new_line.scheduled_date = next_date
                new_line.create_maintenance_request()
                new_ids.append(new_line.id)
                next_date = record._get_next_date(next_date)
            record.state = 'in_process'
            record.line_ids = new_ids

    def generate_maintenance_schedule(self):
        '''Use the pandas function date_range and generates
        maitenance_requests according frequency'''
        for record in self:
            record.line_ids = [(5, 0, 0)]
            start_date = record.start_date
            limit_date = record.limit_date
            freq = ''
            if record.new_frequency_id.years > 0:
                freq = pd.DateOffset(years=record.new_frequency_id.years)
            elif record.new_frequency_id.months > 0:
                freq = pd.DateOffset(months=record.new_frequency_id.months)
            elif record.new_frequency_id.weeks > 0:
                freq = pd.DateOffset(weeks=record.new_frequency_id.weeks)
            elif record.new_frequency_id.days > 0:
                freq = pd.DateOffset(days=record.new_frequency_id.days)
            dRan1 = pd.bdate_range(start=start_date, end=limit_date, freq=freq)
            new_ids = []
            for date in dRan1:
                new_line = self.env['mgmtsystem.maintenance.line'].create({
                    'maintenance_id': record.id,
                    'name': record.name + " " + date.strftime('%d/%m/%Y'),
                })
                new_line.scheduled_date = date
                new_line.create_maintenance_request()
                new_ids.append(new_line.id)
            record.state = 'in_process'
            
            record.line_ids = new_ids
            


    def mail_reminder(self):
        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        for i in match:
            for his in i.line_ids:
                if his.scheduled_date:
                    exp_date = fields.Date.from_string(his.scheduled_date)
                    if date_now == exp_date:
                        mail_content = "  Saludos  " + i.employee_id.name + ",<br>Hay un mantenimiento programado de:  " + i.name + " para " + \
                            str(his.scheduled_date)
                        main_content = {
                            'subject': _('Mantenimiento programado-%s el %s') % (i.name, his.scheduled_date),
                            'author_id': self.env.user.partner_id.id,
                            'body_html': mail_content,
                            'email_to': i.employee_id.user_id.login,
                        }
                        self.env['mail.mail'].create(main_content).send()


class MaintenanceLine(models.Model):
    _name = 'mgmtsystem.maintenance.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Historial de mantenimiento"

    # Fechas de mantenimientos
    maintenance_id = fields.Many2one(
        string='Mantenimiento',
        comodel_name='mgmtsystem.maintenance',
        ondelete='cascade',
    )
    name = fields.Char(
        string='Nombre',
        default='Historial de mantenimiento',
    )
    scheduled_date = fields.Date(
        string='Fecha prevista',
    )
    maintenance_request_ids = fields.One2many(
        string='Peticiones de mantenimiento',
        comodel_name='maintenance.request',
        inverse_name='maintenance_line_id',
    )

    def create_maintenance_request(self):
        for record in self:
            if not record.maintenance_id.equipment_ids:
                return
            user = record.maintenance_id.employee_id.user_id or record.maintenance_id.employee_id.parent_id.user_id or record.maintenance_id.employee_id.coach_id.user_id
            request_ids = []
            for equipment in record.maintenance_id.equipment_ids:
                if record.maintenance_id.plan_id and record.maintenance_id.plan_id.elaboration_step:
                    responsable_id = record.maintenance_id.plan_id.elaboration_step[0].user_id.id
                elif record.maintenance_id.elaboration_step:
                    responsable_id = record.maintenance_id.elaboration_step[0].user_id.id
                else:
                    raise UserError(_('No es posible crear la petición de mantenimiento, no se ha definido usuarios de elaboración.'))
                new_request = self.env['maintenance.request'].create({
                    'name': record.maintenance_id.name+"/"+equipment.name,
                    'responsable_id': responsable_id,
                    'equipment_id': equipment.id,
                    'category_id': equipment.category_id.id if equipment.category_id else False,
                    'schedule_date': record.scheduled_date,
                    'request_date': fields.Date.context_today(self),
                    'maintenance_type': 'preventive',
                    'user_id': equipment.technician_user_id.id,
                    'state': '2approved',
                    'type_line': 'maintenance',
                    'maintenance_line_id': record.id,
                })
                request_ids.append(new_request.id)
                equipment.write(
                    {'request_maintenance_m_ids': [(4, new_request.id)]})
            record.maintenance_request_ids = request_ids


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    maintenance_line_id = fields.Many2one(
        string='Linea de mantenimiento',
        comodel_name='mgmtsystem.maintenance.line',
        ondelete='cascade',
    )
    calibration_line_id = fields.Many2one(
        string='Linea de calibración',
        comodel_name='mgmtsystem.calibration.line',
        ondelete='cascade',
    )
    type_line = fields.Selection(
        string='Tipo de origen',
        selection=[
            ('maintenance', 'Mantenimiento'),
            ('calibration', 'Calibración')
        ],
        default='maintenance',
    )
    cost = fields.Float(string='Costo', digits=(16, 2))

    responsable_id = fields.Many2one(
        comodel_name='res.users', string='Encargado de validación', required=True)


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    property_type = fields.Selection([
        ('own', 'Propio'),
        ('thirdparty', 'Tercero'),
    ], string='Propiedad del equipo')

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado')

    department_id = fields.Many2one(
        string=u'Departamento',
        comodel_name='hr.department',
        ondelete='restrict',
    )

    request_maintenance_m_ids = fields.Many2many(
        'maintenance.request', string='Peticiones de Mantenimientos', relation='main_eqp_req_main')
    request_calibration_m_ids = fields.Many2many(
        'maintenance.request', string='Peticiones de Calibraciones', relation='cal_eqp_req_cal')

    maintenance_m_ids = fields.Many2many(
        'mgmtsystem.maintenance', string='Mantenimientos', relation='main_eqp_rel')
    calibration_m_ids = fields.Many2many(
        'mgmtsystem.calibration', string='Calibraciones', relation='cal_eqp_rel')

    maintenance_count = fields.Integer(
        string="# de mantenimientos", compute='_compute_maintenance_count')

    def _compute_maintenance_count(self):
        for record in self:
            maintenance_count = self.env['maintenance.request'].search_count(
                [('equipment_id', '=', record.id), ('type_line', '=', 'maintenance')]) or 0
            print(maintenance_count)
            record.maintenance_count = maintenance_count

    calibration_count = fields.Integer(
        string="# de calibración", compute='_compute_calibration_count')

    def _compute_calibration_count(self):
        for record in self:
            calibration_count = self.env['maintenance.request'].search_count(
                [('equipment_id', '=', record.id), ('type_line', '=', 'calibration')]) or 0
            record.calibration_count = calibration_count

    def maintenance_action(self):
        action = self.env.ref(
            'mgmtsystem_infrastructure.hr_calibration_request_action').read()[0]
        type_maintenance = self.env.context.get('type_maintenance')
        equipment_id = self.env.context.get('default_equipment_id')
        if type_maintenance == 'maintenance':
            action['context'] = {
                'default_user_id': self.env.user,
                'default_type_line': 'maintenance',
                'default_equipment_id': equipment_id,
            }
            action['domain'] = [
                ('type_line', '=', 'maintenance'), ('equipment_id', '=', equipment_id)]
        elif type_maintenance == 'calibration':
            action['context'] = {
                'default_user_id': self.env.user,
                'default_type_line': 'calibration',
                'default_equipment_id': equipment_id,
            }
            action['domain'] = [
                ('type_line', '=', 'calibration'), ('equipment_id', '=', equipment_id)]
        return action
