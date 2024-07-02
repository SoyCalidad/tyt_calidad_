# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class NCLine(models.TransientModel):
    _name = 'wizard.create.nc.line'
    _description = u'Linea de No conformidades'

    name = fields.Char(u'Nombre',
                       required=True,
                       )
    nc_id = fields.Many2one(
        string=u'W_NC',
        comodel_name='wizard.create.nc'
    )
    employee_id = fields.Many2one(
        string=u'Responsable',
        comodel_name='hr.employee',
        ondelete='cascade',
    )
    auditor_id = fields.Reference(selection=[('res.partner', 'Auditor externo'), (
        'hr.employee', 'Auditor interno'), ], string="Auditor")
    team_id = fields.Many2one(
        string=u'Equipo',
        comodel_name='audit.team',
        ondelete='cascade',
    )
    date_found = fields.Date(
        string=u'Fecha de hallazgo',
        default=fields.Date.context_today,
        required=True,
    )
    date_limit = fields.Date(
        string=u'Fecha límite',
        default=fields.Date.context_today,
    )
    type_id = fields.Many2one('mgmtsystem.nonconformity.type',
                              string='Tipo')
    type = fields.Selection([
        ('key', 'value')
    ], string='s')
    standard = fields.Char(
        string=u'Requisito de la norma',
    )
    process_id = fields.Many2one(
        string=u'Doc.Ref',
        comodel_name='mgmt.process',
        ondelete='cascade',
        domain=[('active','=',True)]
    )
    details = fields.Text(
        string=u'Alcance',
    )


class NC(models.TransientModel):
    _name = 'wizard.create.nc'
    _description = u'Creación de No conformidades'

    report_id = fields.Many2one(
        string=u'Informe',
        comodel_name='audit.report',
        ondelete='cascade',
    )
    wline_ids = fields.One2many(
        string=u'W Lineas',
        comodel_name='wizard.create.nc.line',
        inverse_name='nc_id',
    )

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
                }
                datas.append((0, 0, data))
        self.wline_ids = datas

    def create_nonconformity(self):
        for line in self.wline_ids:
            details = line.details or '-'
            if line.auditor_id:
                auditor_id = line.auditor_id.id
            else:
                auditor_id = None
            if line.team_id:
                team_id = line.team_id.id
            else:
                team_id = None
            data = {
                'report_id': self.report_id.id,
                'name': line.name,
                'reference': line.standard,
                'employee_id': line.employee_id.id,
                'partner_id': auditor_id,
                'description': details,
                'process_id': line.process_id.id,
                'audit_team_id': team_id,
                'date_found': line.date_found,
                'date_limit': line.date_limit,
                'type_id': line.type_id.id,
            }
            self.env['mgmtsystem.nonconformity'].create(data)
        self.report_id.write({'state': 'in_process'})
