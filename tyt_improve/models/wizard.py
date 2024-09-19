# -*- coding: utf-8 -*-


from datetime import datetime

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError


class NCLine(models.TransientModel):
    _inherit = 'wizard.create.nc.line'

    found_description = fields.Text(u'Descripción')


class NC(models.TransientModel):
    _inherit = 'wizard.create.nc'

    '''
    @api.onchange('report_id')
    def _onchange_report_id(self):
        datas = [(5, 0, 0)]
        lines = self.env['report.line'].search(
            [('report_id', '=', self.report_id.id)])
        for line in lines:
            if line.nc_id:
                if self.report_id.auditor_id:
                    print (self.report_id.auditor_id)
                    auditor_id = self.report_id.auditor_id
                else:
                    auditor_id = None
                if self.report_id.team_id:
                    team_id = self.report_id.team_id.id
                else:
                    team_id = None
                data = {
                    'name': line.name,
                    'nc_id': self.id,
                    'auditor_id': auditor_id,
                    'team_id': team_id,
                    'type_id': line.nc_id.id,
                    'standard': self.report_id.standard,
                    'date_found': line.datetime,
                    'found_description': line.found,
                }
                datas.append((0, 0, data))
        self.wline_ids = datas
    '''


    def create_nonconformity(self):
        for line in self.wline_ids:
            auditor_id = line.auditor_id.id if line.auditor_id else False
            team_id = line.team_id.id if line.team_id else False
            
            # Asignación de la descripción encontrada
            found_description = line.found_description or False

            data = {
                'report_id': self.report_id.id,
                'name': line.name,
                'reference': line.standard,
                'employee_id': line.employee_id.id,
                'partner_id': auditor_id,
                'description': line.details or '-',
                'process_id': line.process_id.id,
                'audit_team_id': team_id,
                'date_found': line.date_found,
                'date_limit': line.date_limit,
                'type_id': line.type_id.id,
                'found_description': found_description,  # Agregar 'found_description'
            }

            self.env['mgmtsystem.nonconformity'].create(data)

        # Cambia el estado del informe de auditoría a 'in_process'
        self.report_id.write({'state': 'in_process'})