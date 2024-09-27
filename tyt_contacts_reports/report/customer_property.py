import base64
import io

from odoo import fields, models
from PIL import Image
from datetime import datetime

import io
import base64
from PIL import Image
from odoo.modules.module import get_module_resource


class CustomerPropertyXlsxReport(models.AbstractModel):
    _name = 'report.customer_property_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        white_bg_format = workbook.add_format({'bg_color': '#FFFFFF', 'border': 0})
        format_title = workbook.add_format(
            {'font_size': 22, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vcenter', 'align': 'center',
             'bold': True, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_header_left = workbook.add_format(
            {'font_size': 12, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vcenter', 'align': 'left',
             'bold': True,
             'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_cell_left = workbook.add_format(
            {'font_size': 12, 'align': 'left', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})

        sheet = workbook.add_worksheet('Clientes')
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

        sheet.merge_range(2, 3, 4, 6, 'PROPIEDAD DE LOS CLIENTES', format_title)

        row = 8
        sheet.merge_range(row, 1, row + 1, 1, 'Fecha', format_header_left)
        sheet.merge_range(row, 2, row + 1, 2, 'Cliente-proyecto-plaza', format_header_left)
        sheet.merge_range(row, 3, row + 1, 3, 'Propiedad', format_header_left)
        sheet.merge_range(row, 4, row + 1, 4, 'Actividad de cuidado de la propiedad del cliente', format_header_left)
        sheet.merge_range(row, 5, row + 1, 5, 'Estado inadecuado de la propiedad', format_header_left)
        sheet.merge_range(row, 6, row + 1, 6, 'Actividad de respuesta', format_header_left)

        sheet.merge_range(row, 7, row, 8, 'Medida correctiva iniciada ', format_header_left)
        sheet.write(row + 1, 7, 'Sí', format_title)
        sheet.write(row + 1, 8, 'No', format_title)

        sheet.set_column('B:I', 20)
        sheet.set_column('C:E', 30)
        sheet.set_column('I:I', 50)







