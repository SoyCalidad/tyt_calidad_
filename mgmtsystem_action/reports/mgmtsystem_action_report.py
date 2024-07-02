import base64
import io
import time
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from odoo.addons.hola_calidad.utils.html_utils import HTMLFilter


import pytz
from bs4 import BeautifulSoup
from odoo import _, api, exceptions, fields, models, tools
from odoo.exceptions import UserError
from odoo.http import request
from PIL import Image


class ActionReportXLS(models.AbstractModel):
    _name = 'report.mgmtsystem_action.report_action_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, actions):
        # estilos
        format21_c_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EFEFEF', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
        format21_gray = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        format21_gray_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, })
        format26_c_bold = workbook.add_format(
            {'font_size': 26, 'bg_color': '#EFEFEF', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})

        format21_c_bold.set_border()
        format21_left.set_border()
        format21_gray.set_border()
        format21_gray_bold.set_border()
        format26_c_bold.set_border()

        sheet = workbook.add_worksheet('REGISTRO DE NO CONFORMIDAD',)

        company_id = self.env.user.company_id

        buf_image = io.BytesIO(base64.b64decode(company_id.logo))
        im = Image.open(buf_image)
        width, height = im.size
        image_width = width
        image_height = height
        cell_width = 80
        cell_height = 60

        x_scale = cell_width/image_width
        y_scale = cell_height/image_height
        sheet.insert_image('B2:B3', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 25})

        format21 = workbook.add_format(
            {'font_size': 35, 'align': 'center', 'bold': True})
        format13 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'bold': True})

        # cabecera
        sheet.merge_range('B2:C5', '', format21_c_bold)
        sheet.merge_range('D2:I5', 'REGISTRO DE ACCIONES', format26_c_bold)
        sheet.merge_range('J2:K3', 'MOD', format21_c_bold)
        sheet.merge_range('J4:K5', 'EDICION -', format21_c_bold)

        # cabecera2
        format13.set_border()
        format21.set_border()
        sheet.set_column(0, 0, 10)
        sheet.set_column(7, 6, 18)
        sheet.set_column(7, 1, 24)
        sheet.set_column(6, 2, 24)
        sheet.set_column(7, 5, 30)
        sheet.set_column(7, 14, 30)
        sheet.set_column(8, 14, 20)
        sheet.set_column(8, 16, 20)
        sheet.set_column(8, 18, 30)
        sheet.set_column(8, 20, 25)
        sheet.set_column(8, 21, 30)
        sheet.merge_range('B7:B8', 'FECHA DE APERTURA', format21_gray_bold)
        sheet.merge_range('C7:C8', 'NOMBRE', format21_gray_bold)
        sheet.merge_range('D7:D8', 'TIPO', format21_gray_bold)
        sheet.merge_range('E7:E8', 'REFERENCIA', format21_gray_bold)
        sheet.merge_range('F7:F8', 'RESPONSABLE DE EJECUCIÓN',
                          format21_gray_bold)
        sheet.merge_range(
            'G7:G8', 'RESPONSABLE DE SEGUIMIENTO', format21_gray_bold)
        sheet.merge_range('H7:H8', 'FECHA LÍMITE', format21_gray_bold)
        sheet.merge_range('I7:I8', 'DESCRIPCIÓN', format21_gray_bold)
        sheet.merge_range('J7:J8', 'IDENTIFICADOR', format21_gray_bold)
        sheet.merge_range('K7:K8', 'ESTADO', format21_gray_bold)

        column = 0
        column = column+1
        line = 8

        for nc in actions:
            f = HTMLFilter()
            f.feed(nc.description)
            sheet . set_row(line, 30)
            sheet.write(line, column, str(nc.date_open), format21_left)
            sheet.write(line, column+1, nc.name, format21_left)
            sheet.write(line, column+2, nc.type_action_id.name, format21_left)
            sheet.write(line, column+3, nc.reference, format21_left)
            sheet.write(line, column+4, nc.user_id.name, format21_left)
            sheet.write(line, column+5, nc.track_user_id.name, format21_left)
            sheet.write(line, column+6, str(nc.date_deadline), format21_left)
            sheet.write(line, column+7, f.text, format21_left)
            sheet.write(line, column+8, nc.system_id.name, format21_left)
            sheet.write(
                line, column+9, dict(nc._fields['state'].selection).get(nc.state), format21_left)
            line = line+1


# class MgmtsystemtActionReport(models.Model):
#     """Management System Action Report."""

#     _name = "mgmtsystem.action.report"
#     _auto = False
#     _description = "Management System Action Report"
#     _rec_name = 'id'

#     # Compute data
#     number_of_actions = fields.Integer('# of actions', readonly=True)
#     age = fields.Integer('Age', readonly=True)
#     number_of_days_to_open = fields.Integer('# of days to open', readonly=True)
#     number_of_days_to_close = fields.Integer(
#         '# of days to close', readonly=True)
#     number_of_exceedings_days = fields.Integer(
#         '# of exceedings days', readonly=True)

#     # Grouping view
#     type_action = fields.Selection([
#         ('immediate', 'Immediate Action'),
#         ('correction', 'Corrective Action'),
#         ('prevention', 'Preventive Action'),
#         ('improvement', 'Improvement Opportunity')
#     ], 'Response Type')
#     type_action_id = fields.Many2one('mgmtsystem.action.type', string='Tipo')
#     create_date = fields.Datetime('Create Date', readonly=True, index=True)
#     date_open = fields.Datetime('Fecha de apertura', readonly=True, index=True)
#     date_closed = fields.Datetime('Fecha de cierre', readonly=True, index=True)
#     date_deadline = fields.Date('Deadline', readonly=True, index=True)
#     user_id = fields.Many2one('res.users', 'User', readonly=True)
#     state = fields.Selection(
#         string=u'Estado',
#         selection=[('open', 'Abierto'),
#                    ('follow', 'En seguimiento'),
#                    ('done', 'Cerrado'),
#                    ('cancel', 'Cancelado')],
#         readonly=True
#     )

#     def init(self):
#         """Display a pivot view of action."""
#         tools.drop_view_if_exists(self._cr, 'mgmtsystem_action_report')
#         self.env.cr.execute("""
#              CREATE OR REPLACE VIEW mgmtsystem_action_report AS (
#                  select
#                     m.id,
#                     m.date_closed as date_closed,
#                     m.date_deadline as date_deadline,
#                     m.date_open as date_open,
#                     m.user_id,
#                     m.state,
#                     m.type_action_id as type_action_id,
#                     m.create_date as create_date,
#                     m.number_of_days_to_open as number_of_days_to_open,
#                     m.number_of_days_to_close as number_of_days_to_close,
#                     avg(extract('epoch' from (current_date-m.create_date))
#                     )/(3600*24) as  age,
#                     avg(extract('epoch' from (m.date_closed - m.date_deadline))
#                     )/(3600*24) as  number_of_exceedings_days,
#                     count(*) AS number_of_actions
#                 from
#                     mgmtsystem_action m
#                 group by m.user_id, m.state, m.date_open, \
#                         m.create_date,m.type_action_id,m.date_deadline, \
#                         m.date_closed, m.id, m.number_of_days_to_open, \
#                         m.number_of_days_to_close
#             )
#             """)
