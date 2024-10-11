# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

from datetime import tzinfo, date, datetime, timedelta
import pandas as pd
import logging
_logger = logging.getLogger(__name__)

class Plan(models.Model):
    _inherit = "audit.plan"

    # Campo para evitar duplicados
    is_process_started = fields.Boolean(
        string='Proceso Iniciado',
        default=False,
        readonly=True
    )

    def start_process(self):
        for plan in self:
            _logger.info(f"Iniciando el proceso para el plan: {plan.name} (ID: {plan.id})")
            print(f"Iniciando el proceso para el plan: {plan.name} (ID: {plan.id})")

            #if plan.is_process_started:
                #raise UserError(_("El proceso ya ha sido iniciado para este registro."))

            if not plan.audit_plan_tyt_auditor_id:
                raise UserError(_("Debe asignar un 'Cronograma - Auditores' antes de iniciar el proceso."))

            _logger.info(f"Auditor asociado: {plan.audit_plan_tyt_auditor_id.name} (ID: {plan.audit_plan_tyt_auditor_id.id})")
            print(f"Auditor asociado: {plan.audit_plan_tyt_auditor_id.name} (ID: {plan.audit_plan_tyt_auditor_id.id})")

            # Definir los datos de los registros a crear basados en nombres únicos de sitios
            schedule_data = [
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_1').id,
                    'sites_id': self.env['x_sitios'].search([('x_name', '=', 'Guadalajara')], limit=1).id,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_4').id,
                    'sites_id': self.env['x_sitios'].search([('x_name', '=', 'Guadalajara')], limit=1).id,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_1').id,
                    'sites_id': self.env['x_sitios'].search([('x_name', '=', 'Hermosillo')], limit=1).id,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_4').id,
                    'sites_id': self.env['x_sitios'].search([('x_name', '=', 'Hermosillo')], limit=1).id,
                },
            ]

            for data in schedule_data:
                site = self.env['x_sitios'].browse(data['sites_id'])
                _logger.info(f"Procesando sitio: {site.x_name} (ID: {site.id})")
                print(f"Procesando sitio: {site.x_name} (ID: {site.id})")

                existing_schedule = self.env['audit.plan.schedule'].search([
                    ('audit_plan_id', '=', plan.id),
                    ('description_id', '=', data['description_id']),
                    ('activity_id', '=', data['activity_id']),
                    ('sites_id', '=', data['sites_id']),
                ], limit=1)

                if existing_schedule:
                    _logger.info(f"Ya existe un schedule para sitio '{site.x_name}' con ID {existing_schedule.id}.")
                    print(f"Ya existe un schedule para sitio '{site.x_name}' con ID {existing_schedule.id}.")
                    continue  # Omitir la creación si ya existe

                # Obtener los datos de audit.plan.tyt.auditor.schedule según sites_id
                auditor_schedules = plan.audit_plan_tyt_auditor_id.schedule_ids.filtered(
                    lambda s: s.tyt_sites_id.id == data['sites_id']
                )

                # Depuración
                _logger.info(f"Auditor Schedules para sitio ID {data['sites_id']}: {auditor_schedules.ids}")
                print(f"Auditor Schedules para sitio ID {data['sites_id']}: {auditor_schedules.ids}")

                if not auditor_schedules:
                    _logger.warning(f"No hay schedules configurados para el sitio ID {data['sites_id']}.")
                    raise UserError(_("No hay datos de auditoría configurados para el sitio seleccionado."))

                # Calcular total_weeks sumando 'total_sum' de todos los schedules relacionados
                total_weeks = sum(aud.total_sum for aud in auditor_schedules)
                _logger.info(f"Total semanas para sitio ID {data['sites_id']}: {total_weeks}")
                print(f"Total semanas para sitio ID {data['sites_id']}: {total_weeks}")

                # Obtener todos los auditores responsables
                auditors = self.env['res.partner'].browse()
                for aud_schedule in auditor_schedules:
                    auditors |= aud_schedule.responsible_auditors_id

                _logger.info(f"Auditores responsables: {auditors.mapped('name')}")
                print(f"Auditores responsables: {auditors.mapped('name')}")

                # Crear el registro en audit.plan.schedule
                new_schedule = self.env['audit.plan.schedule'].create({
                    'audit_plan_id': plan.id,
                    'description_id': data['description_id'],
                    'activity_id': data['activity_id'],
                    'sites_id': data['sites_id'],
                    'responsible_auditors_id': [(6, 0, auditors.ids)],
                    'total_weeks': total_weeks,
                    'name': f"{plan.name} - Schedule {site.x_name}",
                })

                _logger.info(f"Nuevo schedule creado: ID {new_schedule.id} para el sitio {site.x_name}")
                print(f"Nuevo schedule creado: ID {new_schedule.id} para el sitio {site.x_name}")

            # Marcar el proceso como iniciado
            plan.is_process_started = True

            # Mensaje de confirmación
            plan.message_post(body=_("El proceso ha sido iniciado y los registros de cronograma han sido creados."))

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }