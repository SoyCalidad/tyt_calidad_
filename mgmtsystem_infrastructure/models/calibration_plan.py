# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

from datetime import tzinfo, date, datetime, timedelta
import pandas as pd

class CalibrationPlan(models.Model):
    _name = 'mgmtsystem.calibration.plan'
    _inherit = ['mgmtsystem.maintenance.plan', 'mgmtsystem.code']
    _description = "Programa de calibraciones"

    name = fields.Char(
        string=u'Nombre',
        required=True,
        default="Programa de Calibración"
    )

    maintenance_ids = fields.One2many(
        string='Calibraciones',
        comodel_name='mgmtsystem.calibration',
        inverse_name='plan_id',
        copy=True,
    )
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.calibration.plan', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.calibration.plan', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_infrastructure.mgmtsystem_calibration_plan_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def open_maintenance_ids(self):
        for each in self:
            ids = [x.id for x in each.maintenance_ids]
            result = self.env.ref(
                'mgmtsystem_infrastructure.mgmtsystem_calibration_action').read()[0]
            result['domain'] = [('id', 'in', ids)]
            return result


class Calibration(models.Model):
    _name = 'mgmtsystem.calibration'
    _inherit = ['mgmtsystem.maintenance']
    _description = "Calibración"

    plan_id = fields.Many2one(
        string='Programa de calibraciones',
        comodel_name='mgmtsystem.calibration.plan',
        ondelete='cascade',
    )
    line_ids = fields.One2many(
        string='Lineas',
        comodel_name='mgmtsystem.calibration.line',
        inverse_name='maintenance_id',
    )
    responsable_id = fields.Many2one(
        comodel_name='res.users', string='Creado por', required=False)
    equipment_ids = fields.Many2many(
        string='Equipos',
        comodel_name='maintenance.equipment',
        relation='mgmtsystem_calibration_equipment',
        column1='equipment_id',
        column2='calibration_id',
    )

    max_errors1 = fields.Float(
        string='Unidad',
    )
    max_errors2 = fields.Float(
        string='Unidad',
    )
    signe = fields.Selection(
        string='Signo',
        selection=[
            ('m', '-'),
            ('p', '+'),
            ('mp', '+-')],
        default='mp'
    )
    uom_id = fields.Many2one(
        string='Unidad de medida',
        comodel_name='uom.uom',
        ondelete='cascade',
    )

    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        if not self.uom_id:
            return
        self.uom2_id = self.uom_id

    uom2_id = fields.Many2one(
        string='Unidad de medida',
        comodel_name='uom.uom',
        ondelete='cascade',
    )

    calibration_range = fields.Char(
        string='Rango',
    )
    resolution = fields.Char(
        string='Resolución',
    )
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.calibration', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.calibration', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_infrastructure.mgmtsystem_calibration_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def create_cronograma(self):
        for record in self:
            start_date = record.start_date
            limit_date = record.limit_date
            next_date = record._get_next_date(start_date)
            new_ids = []
            while next_date < limit_date:
                new_line = self.env['mgmtsystem.calibration.line'].create({
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
                new_line = self.env['mgmtsystem.calibration.line'].create({
                    'maintenance_id': record.id,
                    'name': record.name + " " + date.strftime('%d/%m/%Y'),
                })
                new_line.scheduled_date = date
                new_line.create_maintenance_request()
                new_ids.append(new_line.id)
            record.state = 'in_process'
            
            record.line_ids = new_ids

class CalibrationLine(models.Model):
    _name = 'mgmtsystem.calibration.line'
    _inherit = ['mgmtsystem.maintenance.line']
    _description = "Historial de calibraciones"

    maintenance_id = fields.Many2one(
        string='Calibración',
        comodel_name='mgmtsystem.calibration',
        ondelete='cascade',
    )
    maintenance_request_ids = fields.One2many(
        string='Peticiones de mantenimiento',
        comodel_name='maintenance.request',
        inverse_name='calibration_line_id',
    )

    def create_maintenance_request(self):
        for record in self:
            if not record.maintenance_id.equipment_ids:
                return
            user = record.maintenance_id.employee_id.user_id or record.maintenance_id.employee_id.parent_id.user_id or record.maintenance_id.employee_id.coach_id.user_id
            if record.maintenance_id.plan_id and record.maintenance_id.plan_id.elaboration_step:
                responsable_id = record.maintenance_id.plan_id.elaboration_step[0].user_id.id
            elif record.maintenance_id.elaboration_step:
                responsable_id = record.maintenance_id.elaboration_step[0].user_id.id
            else:
                raise UserError(_('No es posible crear la petición de mantenimiento, no se ha definido usuarios de elaboración.'))
            request_ids = []
            for equipment in record.maintenance_id.equipment_ids:
                new_request = self.env['maintenance.request'].create({
                    'name': record.maintenance_id.name+"/"+equipment.name,
                    'responsable_id': responsable_id,
                    'equipment_id': equipment.id,
                    'category_id': equipment.category_id.id if equipment.category_id else False,
                    'schedule_date': record.scheduled_date,
                    'request_date': fields.Date.context_today(self),
                    'maintenance_type': 'preventive',
                    'user_id': user.id,
                    'state': '2approved',
                    'type_line': 'calibration',
                    'calibration_line_id': record.id,
                })
                request_ids.append(new_request.id)
                equipment.write(
                    {'request_calibration_m_ids': [(4, new_request.id)]})
            record.maintenance_request_ids = request_ids
