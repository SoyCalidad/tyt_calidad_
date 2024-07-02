# -*- coding: utf-8 -*-

import base64
import io
from collections import defaultdict
from PIL import Image
from odoo import models, fields
from math import ceil


class NonconformityOutputReport(models.AbstractModel):
    _name = 'report.report_nonconformity_output'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, nonconformities):
        """Generate a xls report with the data

        Arguments:
            workbook {object} -- A object that represents a Excel workbook
            data {dict} -- The data of the report
            nonconformities {object} -- A class object
        """

        format_title = workbook.add_format(
            {'font_size': 15, 'bg_color': '#D3D3D3', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': 1})
        format_data = workbook.add_format(
            {'font_size': 9, 'font_name': 'Arial', 'text_wrap': True, 'border': 1})
        format_header = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 1, 'bg_color': '#D3D3D3'})

        sheet = workbook.add_worksheet('Salidas NC')
        company_id = self.env.user.company_id

        buf_image = io.BytesIO(base64.b64decode(company_id.logo))
        im = Image.open(buf_image)
        old_width, old_height = im.size
        im.thumbnail((100, 100))
        width, height = im.size
        x_scale = width / old_width
        y_scale = height / old_height

        sheet.insert_image('A1', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 45, 'y_offset': 15})

        code = ''
        version = ''
        date = fields.Date.today().strftime('%d/%m/%Y')

        sheet.merge_range(0, 0, 2, 0, '', format_header)
        sheet.merge_range(
            0, 1, 2, 3, 'REPORTE DE SALIDAS NO CONFORMES Y ACCIONES PARA EL TRATAMIENTO', format_title)
        sheet.write(0, 4, 'Código: %s' % code, format_header)
        sheet.write(1, 4, 'Versión: %s' % version, format_header)
        sheet.write(2, 4, 'Fecha de elaboración: %s' % date, format_header)

        row = 4

        sheet.set_row(row, 30)
        sheet.set_column(0, 8, 25)

        sheet.write(row, 0, 'Proceso', format_header)
        sheet.write(row, 1, 'Nombre', format_header)
        sheet.write(row, 2, 'Fuente', format_header)
        sheet.write(row, 3, 'Fecha de hallazgo', format_header)
        sheet.write(row, 4, 'Tipo de acción', format_header)
        sheet.write(row, 5, 'Autoridad que aprueba la acción', format_header)
        sheet.write(row, 6, 'Acciones tomadas', format_header)
        sheet.write(row, 7, 'Fecha propuesta de cierre', format_header)
        sheet.write(row, 8, 'Fecha real de cierre', format_header)
        row += 1
        for each in nonconformities:
            if len(each.action_ids) > 1:
                sheet.merge_range(
                    row, 0, row + len(each.action_ids) - 1, 0, each.process_id.name, format_data)
                sheet.merge_range(
                    row, 1, row + len(each.action_ids) - 1, 1, each.name, format_data)
                sheet.merge_range(
                    row, 2, row + len(each.action_ids) - 1, 2, each.source, format_data)
                sheet.merge_range(
                    row, 3, row + len(each.action_ids) - 1, 3, each.date_found, format_data)
            else:
                sheet.write(row, 0, each.process_id.name, format_data)
                sheet.write(row, 1, each.name, format_data)
                sheet.write(row, 2, each.source, format_data)
                date_found = each.date_found.strftime(
                    '%d/%m/%Y') if each.date_found else ''
                sheet.write(row, 3, date_found, format_data)
            for action in each.action_ids:
                sheet.write(
                    row, 4, action.type_action_id.name if action.type_action_id else '', format_data)
                sheet.write(
                    row, 5, action.approving_authority_id.name if action.approving_authority_id else '', format_data)
                sheet.write(row, 6, action.name, format_data)
                date_deadline = action.date_deadline.strftime(
                    '%d/%m/%Y') if action.date_deadline else ''
                date_closed = action.date_closed.strftime(
                    '%d/%m/%Y') if action.date_closed else ''
                sheet.write(row, 7, date_deadline, format_data)
                sheet.write(row, 8, date_closed, format_data)
                height = len(action.name)
                if height > 25:
                    height = ceil(height/25)*10
                sheet.set_row(row, height)
                row += 1
            if not each.action_ids:
                sheet.write(row, 4, '', format_data)
                sheet.write(row, 5, '', format_data)
                sheet.write(row, 6, '', format_data)
                sheet.write(row, 7, '', format_data)
                sheet.write(row, 8, '', format_data)
                row += 1
        workbook.close()
