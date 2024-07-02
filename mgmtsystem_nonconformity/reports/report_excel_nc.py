
import base64
import io
from PIL import Image
from odoo import models

from collections import defaultdict
import pytz
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


class Report_excel_nc(models.AbstractModel):
    _name = 'report.report_excel_nc.xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Registro de no conformidades'

    def generate_xlsx_report(self, workbook, data, lines):
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

        sheet.merge_range('B2:C5', '', format21_c_bold)
        sheet.merge_range(
            'D2:G5', 'REGISTRO DE NO CONFORMIDAD', format26_c_bold)
        model_id = self.env['ir.model'].search(
            [('model', '=', self._name)],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code else ''
        sheet.merge_range('H2:I3', 'Código: ' + code, format21_c_bold)
        sheet.merge_range('H4:I4', 'Versión: 1', format21_c_bold)
        sheet.write('H5', 'Fecha inicio: ' +
                    data['form']['date_init'], format21_c_bold)
        sheet.write('I5', 'Fecha fin: ' +
                    data['form']['date_fin'], format21_c_bold)
        sheet.merge_range('B6:E6', 'INFORMACIÓN', format21_c_bold)
        sheet.merge_range('F6:H6', 'FORMULACION', format21_c_bold)
        sheet.write('I6', '', format21_c_bold)

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
        sheet.merge_range('B7:B8', 'FECHA DE HALLAZGO', format21_gray_bold)
        sheet.merge_range('C7:C8', 'NOMBRE', format21_gray_bold)
        sheet.merge_range('D7:D8', 'TIPO', format21_gray_bold)
        sheet.merge_range('E7:E8', 'REQUISITOS DE LA NORMA',
                          format21_gray_bold)
        sheet.merge_range('F7:F8', 'RESPONSABLE', format21_gray_bold)
        sheet.merge_range('G7:G8', 'AUTOR', format21_gray_bold)
        sheet.merge_range('H7:H8', 'AUDITOR', format21_gray_bold)
        sheet.merge_range('I7:I8', 'ESTADO', format21_gray_bold)

        column = 0
        column = column+1
        line = 8

        action_nc = self.env['mgmtsystem.nonconformity'].search([
            ('date_found', '>=', data['form']['date_init']),
            ('date_found', '<=', data['form']['date_fin'])
        ], order="date_found asc")

        for nc in action_nc:
            sheet . set_row(line, 30)
            sheet.write(line, column, str(nc.date_found), format21_left)
            sheet.write(line, column+1, nc.name, format21_left)
            sheet.write(line, column+2, nc.type_id.name, format21_left)
            sheet.write(
                line, column+3, ', '.join(nc.iso_9001_requeriments_ids.mapped('name')), format21_left)
            sheet.write(line, column+4, nc.employee_id.name, format21_left)
            sheet.write(line, column+5, nc.user_id.name, format21_left)
            sheet.write(line, column+6, nc.partner_id.name, format21_left)
            sheet.write(
                line, column+7, dict(nc._fields['state'].selection).get(nc.state), format21_left)

            line = line+1


class Report_excel_nc_ac(models.AbstractModel):
    _name = 'report.report_excel_nc_ac.xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Registro de no conformidades y acciones'

    def generate_xlsx_report(self, workbook, data, lines):
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

        sheet = workbook.add_worksheet(
            'REGISTRO DE NO CONFORMIDADES Y ACCIONES',)

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
        model_id = self.env['ir.model'].search(
            [('model', '=', self._name)],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code else ''
        sheet.merge_range('B2:C5', '', format21_c_bold)
        sheet.merge_range(
            'D2:L5', 'REGISTRO DE NO CONFORMIDADES Y ACCIONES', format26_c_bold)
        sheet.merge_range('M2:N3', 'Código: ' + code, format21_c_bold)
        sheet.merge_range('M4:N4', 'Versión: 1', format21_c_bold)
        validation_date = data['form']['validation_date'].strftime(
            '%d/%m/%Y') if data['form']['validation_date'] else ''
        sheet.merge_range('M5:N5', 'Fecha de validación: ' +
                          validation_date, format21_c_bold)
        sheet.merge_range('B6:E6', 'IDENTIFICACION', format21_c_bold)
        sheet.merge_range('F6:J6', 'FORMULACION', format21_c_bold)
        sheet.merge_range('K6:N6', 'SEGUIMIENTO', format21_c_bold)

        # cabecera2
        format13.set_border()
        format21.set_border()

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
        sheet.merge_range('B7:B8', 'FECHA DE HALLAZGO', format21_gray_bold)
        sheet.merge_range('C7:C8', 'NOMBRE', format21_gray_bold)
        sheet.merge_range('D7:D8', 'ORIGEN', format21_gray_bold)
        sheet.merge_range('E7:E8', 'DESCRIPCIÓN', format21_gray_bold)
        sheet.merge_range('F7:F8', 'ACCIONES A EMPRENDER', format21_gray_bold)
        sheet.merge_range('G7:G8', 'TIPO', format21_gray_bold)
        sheet.merge_range('H7:H8', 'ESTADO DE LAS ACCIONES',
                          format21_gray_bold)
        sheet.merge_range('I7:I8', 'FECHA DE CIERRE', format21_gray_bold)
        sheet.merge_range('J7:J8', 'REINCIDENCIA', format21_gray_bold)
        sheet.merge_range('K7:K8', 'FECHA DE SEGUIMIENTO', format21_gray_bold)
        sheet.merge_range(
            'L7:L8', 'RESULTADO DE VERIFICACION', format21_gray_bold)
        sheet.merge_range('M7:M8', 'EFECTIVIDAD %', format21_gray_bold)
        sheet.merge_range('N7:N8', 'EVIDENCIA DE LA EFICACIA',
                          format21_gray_bold)

        column = 0
        column = column+1
        line = 8

        action_nc = self.env['mgmtsystem.nonconformity'].search([
            ('date_found', '>=', data['form']['date_init']),
            ('date_found', '<=', data['form']['date_fin'])
        ], order="date_found asc")

        for nc in action_nc:
            sheet . set_row(line, 30)

            sheet.write(line, column, str(nc.date_found), format21_left)
            sheet.write(line, column+1, nc.name, format21_left)
            sheet.write(
                line, column+2, (', '.join(x.origin_model_id.name for x in nc.origin_ids)), format21_left)
            sheet.write(line, column+3, BeautifulSoup(nc.description,
                        'lxml').get_text(), format21_left)
            actions = dates = types = states = ""
            for action in nc.action_ids:
                actions = actions+str(action.name)+","
                dates = dates + \
                    str(action.date_follow if action.date_follow else "Sin definir")+","
                type_action_name = dict(
                    action._fields['type_action'].selection).get(action.type_action)
                types = types+str(type_action_name)+","
                state_name = dict(
                    action._fields['state'].selection).get(action.state)
                states = states+str(state_name)+","

            # accion a emprender
            sheet.write(line, column+4, actions, format21_left)
            sheet.write(line, column+5, types, format21_left)
            sheet.write(line, column+6, states, format21_left)
            sheet.write(line, column+7, str(nc.date_limit), format21_left)
            sheet.write(line, column+8, nc.count_origin_ids, format21_left)
            sheet.write(line, column+9, str(dates), format21_left)
            sheet.write(line, column+10, "", format21_left)
            sheet.write(line, column+11, "", format21_left)
            sheet.write(line, column+12, "", format21_left)
            line = line+1
