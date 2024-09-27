import base64
import io

from odoo import fields, models
from PIL import Image
from datetime import datetime

import io
import base64
from PIL import Image
from odoo.modules.module import get_module_resource


class SupplierEvaluationVerificationXlsxReport(models.AbstractModel):
    _name = 'report.supplier_evaluation_verification_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        white_bg_format = workbook.add_format({'bg_color': '#FFFFFF', 'border': 0})
        format_title = workbook.add_format(
            {'font_size': 22, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vcenter', 'align': 'center',
             'bold': True, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_header_left = workbook.add_format(
            {'font_size': 11, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vcenter', 'align': 'left',
             'bold': True,
             'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_header_center = workbook.add_format(
            {'font_size': 11, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vcenter', 'align': 'center',
             'bold': True, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})

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

        row = 2
        sheet.merge_range(row, 3, row, 7, 'LISTA DE VERIFICACIÓN PARA EVALUACIÓN DE PROVEEDORES', format_title)

        row = 1
        sheet.merge_range(row, 9, row, 11, 'REFERENCIAS', format_header_center)
        row += 1
        sheet.write(row, 9, 'Símbolo', format_header_left)
        sheet.write(row, 10, 'Criterios', format_header_left)
        sheet.write(row, 11, 'Rango de puntaje', format_header_left)
        row += 1
        sheet.write(row, 9, 'CE', format_cell_left)
        sheet.write(row, 10, 'Calidad de envío', format_cell_left)
        sheet.write(row, 11, 'de 0 a 30', format_cell_left)
        row += 1
        sheet.write(row, 9, 'P', format_cell_left)
        sheet.write(row, 10, 'Precio', format_cell_left)
        sheet.write(row, 11, 'de 0 a 25', format_cell_left)
        row += 1
        sheet.write(row, 9, 'CP', format_cell_left)
        sheet.write(row, 10, 'Confiabilidad del proveedor', format_cell_left)
        sheet.write(row, 11, 'de 0 a 20', format_cell_left)
        row += 1
        sheet.write(row, 9, 'TP', format_cell_left)
        sheet.write(row, 10, 'Términos de pago', format_cell_left)
        sheet.write(row, 11, 'de 0 a 15', format_cell_left)
        row += 1
        sheet.write(row, 9, 'TE', format_cell_left)
        sheet.write(row, 10, 'Tiempo de entrega', format_cell_left)
        sheet.write(row, 11, 'de 0 a 10', format_cell_left)

        row = 6
        sheet.write(row, 1, 'Año', format_header_left)
        sheet.write(row, 2, '', format_cell_left)

        row = 11
        sheet.merge_range(row, 1, row + 4, 1, 'No.', format_header_center)
        sheet.merge_range(row, 2, row + 4, 2, 'Proveedor', format_header_center)
        sheet.merge_range(row, 3, row + 4, 3, 'Tipo de bienes / servicio', format_header_center)
        sheet.merge_range(row, 4, row + 4, 4, 'CE', format_header_center)
        sheet.merge_range(row, 5, row + 4, 5, 'P', format_header_center)
        sheet.merge_range(row, 6, row + 4, 6, 'CP', format_header_center)
        sheet.merge_range(row, 7, row + 4, 7, 'TP', format_header_center)
        sheet.merge_range(row, 8, row + 4, 8, 'TE:', format_header_center)
        sheet.merge_range(row, 9, row + 4, 9, 'Total:', format_header_center)


        sheet.write(row, 10, 'Calificación', format_header_center)
        row += 1
        sheet.write(row, 10, 'A – Excepcional', format_header_center)
        row += 1
        sheet.write(row, 10, 'B – Aceptable', format_header_center)
        row += 1
        sheet.write(row, 10, 'C – Aceptable con prueba adicional', format_header_center)
        row += 1
        sheet.write(row, 10, 'D – Inaceptable', format_header_center)


        sheet.set_column('B:I', 20)
        sheet.set_column('C:C', 30)
        sheet.set_column('E:F', 30)
        sheet.set_column('I:I', 30)
        sheet.set_column('K:K', 35)





