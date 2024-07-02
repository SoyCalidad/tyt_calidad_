# # -*- coding: utf-8 -*-

# from odoo import models, fields, api, _
# from odoo.exceptions import UserError, RedirectWarning, ValidationError


# class NCLine(models.TransientModel):
#     _name = 'wizard.create.nc.line'
#     _description = u'Linea de No conformidades'

#     name = fields.Char(u'Nombre',
#         required=True,
#     )
#     nc_id = fields.Many2one(
#         string=u'W_NC',
#         comodel_name='wizard.create.nc'
#     )
#     employee_id = fields.Many2one(
#         string=u'Responsable',
#         comodel_name='hr.employee',
#         ondelete='cascade',
#     )
#     auditor_id = fields.Many2one(
#         string=u'Auditor',
#         comodel_name='res.partner',
#         required=True,
#     )
#     team_id = fields.Many2one(
#         string=u'Equipo',
#         comodel_name='audit.team',
#         ondelete='cascade',
#     )
#     date_found = fields.Date(
#         string=u'Fecha de hallazgo',
#         default=fields.Date.context_today,
#         required=True,
#     )
#     date_limit = fields.Date(
#         string=u'Fecha límite',
#         default=fields.Date.context_today,
#     )
#     type = fields.Many2one('mgmtsystem.nonconformity.type',
#                            string='Tipo')
#     standard = fields.Char(
#         string=u'Requisito de la norma',
#         required=True,
#     )
#     process_id = fields.Many2one(
#         string=u'Doc.Ref',
#         comodel_name='mgmt.process',
#         ondelete='cascade',
#     )
#     details = fields.Text(
#         string=u'Alcance',
#         required=True,
#     )


# class NC(models.TransientModel):
#     _name = 'wizard.create.nc'
#     _description = u'Creación de No conformidades'

#     report_id = fields.Many2one(
#         string=u'Informe',
#         comodel_name='audit.report',
#         ondelete='cascade',
#     )
#     wline_ids = fields.One2many(
#         string=u'W Lineas',
#         comodel_name='wizard.create.nc.line',
#         inverse_name='nc_id',
#     )

#     @api.onchange('report_id')
#     def _onchange_report_id(self):
#         datas = [(5, 0, 0)]
#         lines = self.env['report.line'].search([('report_id','=',self.report_id.id)])
#         for line in lines:
#             if line.nc:
#                 data = {
#                     'name': line.name,
#                     'nc_id': self.id,
#                     'auditor_id': self.report_id.auditor_id.id,
#                     'team_id': self.report_id.team_id.id,
#                     'type': line.nc.id,
#                     'standard': self.report_id.standard,
#                     'date_found': line.datetime,
#                     'details': line.found,
#                 }
#                 datas.append((0, 0, data))
#         self.wline_ids = datas

#     def create_nonconformity(self):
#         for line in self.wline_ids:
#             data = {
#                 'report_id': self.report_id.id,
#                 'name': line.name,
#                 'reference': line.standard,
#                 'employee_id': line.employee_id.id,
#                 'partner_id': line.auditor_id.id,
#                 'description': line.details,
#                 'process_id': line.process_id.id,
#                 'team_id': line.team_id.id,
#                 'date_found': line.date_found,
#                 'date_limit': line.date_limit,
#             }
#             self.env['mgmtsystem.nonconformity'].create(data)
#         self.report_id.write({'state': 'in_process'})