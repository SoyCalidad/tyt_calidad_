import base64
import io

from odoo import fields, models
from PIL import Image
from datetime import datetime

import io
import base64
from PIL import Image
from odoo.modules.module import get_module_resource


class ApprovedSupplierXlsxReport(models.AbstractModel):
    _name = 'report.approved_supplier_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        white_bg_format = workbook.add_format({'bg_color': '#FFFFFF', 'border': 0})
        format_title = workbook.add_format(
            {'font_size': 36, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vcenter', 'align': 'center',
             'bold': True, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_header_left = workbook.add_format(
            {'font_size': 11, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vcenter', 'align': 'left',
             'bold': True,
             'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_cell_left = workbook.add_format(
            {'font_size': 11, 'align': 'left', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})

        sheet = workbook.add_worksheet('Proveedores')
        sheet.set_column('A:XFD', None, white_bg_format)
        sheet.hide_gridlines(2)

        image_path = get_module_resource('tyt_contacts_reports', 'static/src/img', 'logo.png')
        with open(image_path, 'rb') as f:
            buf_image = io.BytesIO(f.read())
        im = Image.open(buf_image)
        width, height = im.size
        image_width = width
        image_height = height
        cell_width = 150
        cell_height = 124
        x_scale = cell_width / image_width
        y_scale = cell_height / image_height
        sheet.insert_image('B1:B3', "logo.png",
                           {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 10})

        sheet.merge_range(2, 3, 2, 7, 'LISTA DE PROVEEDORES APROBADOS', format_title)

        row = 7
        sheet.write(row, 1, 'NO.', format_header_left)
        sheet.write(row, 2, 'PROVEEDOR', format_header_left)
        sheet.write(row, 3, 'BIENES/SERVICIO', format_header_left)
        sheet.write(row, 4, 'FECHA DE EVALUACIÓN', format_header_left)
        sheet.write(row, 5, 'CALIFICACIÓN', format_header_left)
        sheet.write(row, 6, 'FECHA DE EVALUACIÓN', format_header_left)
        sheet.write(row, 7, 'CALIFICACIÓN', format_header_left)
        sheet.write(row, 8, 'NOTA:', format_header_left)

        sheet.set_column('B:I', 20)
        sheet.set_column('C:C', 30)
        sheet.set_column('E:F', 30)
        sheet.set_column('I:I', 30)
        sheet.set_row(7, 24)





