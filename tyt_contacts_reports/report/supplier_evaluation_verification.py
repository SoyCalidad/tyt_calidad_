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
            {'font_size': 22, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'bottom', 'align': 'center',
             'bold': True, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_header_left = workbook.add_format(
            {'font_size': 12, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vcenter', 'align': 'left',
             'bold': True,
             'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_header_center = workbook.add_format(
            {'font_size': 12, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vcenter', 'align': 'center',
             'bold': True, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_header2_center = workbook.add_format(
            {'font_size': 12, 'color': '#000000', 'bg_color': '#B7DEE8', 'valign': 'vcenter', 'align': 'center',
             'bold': True, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})

        format_cell_left = workbook.add_format(
            {'font_size': 12, 'align': 'left', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})

        format_cell2_left = workbook.add_format(
            {'font_size': 12, 'align': 'left', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': 2,
             'border_color': '#808080'})

        format_cell_14_left = workbook.add_format(
            {'font_size': 14, 'font_name': 'Arial', 'align': 'left', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': 2,
             'border_color': '#808080'})

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
        cell_width = 120
        cell_height = 104
        x_scale = cell_width / image_width
        y_scale = cell_height / image_height
        sheet.insert_image('B1:B3', "logo.png",
                           {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 10})

        row = 2
        sheet.merge_range(row, 3, row, 7, 'LISTA DE VERIFICACIÓN PARA EVALUACIÓN DE PROVEEDORES', format_title)

        row = 1
        sheet.merge_range(row, 9, row, 11, 'REFERENCIAS', format_header2_center)
        row += 1
        sheet.write(row, 9, 'Símbolo', format_header_left)
        sheet.write(row, 10, 'Criterios', format_header_left)
        sheet.write(row, 11, 'Rango de puntaje', format_header_left)
        row += 1
        sheet.write(row, 9, 'CE', format_cell2_left)
        sheet.write(row, 10, 'Calidad de envío', format_cell2_left)
        sheet.write(row, 11, 'de 0 a 30', format_cell2_left)
        row += 1
        sheet.write(row, 9, 'P', format_cell2_left)
        sheet.write(row, 10, 'Precio', format_cell2_left)
        sheet.write(row, 11, 'de 0 a 25', format_cell2_left)
        row += 1
        sheet.write(row, 9, 'CP', format_cell2_left)
        sheet.write(row, 10, 'Confiabilidad del proveedor', format_cell2_left)
        sheet.write(row, 11, 'de 0 a 20', format_cell2_left)
        row += 1
        sheet.write(row, 9, 'TP', format_cell2_left)
        sheet.write(row, 10, 'Términos de pago', format_cell2_left)
        sheet.write(row, 11, 'de 0 a 15', format_cell2_left)
        row += 1
        sheet.write(row, 9, 'TE', format_cell2_left)
        sheet.write(row, 10, 'Tiempo de entrega', format_cell2_left)
        sheet.write(row, 11, 'de 0 a 10', format_cell2_left)

        row = 6
        sheet.write(row, 1, 'Año', format_header_left)
        sheet.write(row, 2, datetime.now().year, format_cell_14_left)

        row = 11
        sheet.merge_range(row, 1, row + 4, 1, 'No.', format_header2_center)
        sheet.merge_range(row, 2, row + 4, 2, 'Proveedor', format_header2_center)
        sheet.merge_range(row, 3, row + 4, 3, 'Tipo de bienes / servicio', format_header2_center)
        sheet.merge_range(row, 4, row + 4, 4, 'CE', format_header2_center)
        sheet.merge_range(row, 5, row + 4, 5, 'P', format_header2_center)
        sheet.merge_range(row, 6, row + 4, 6, 'CP', format_header2_center)
        sheet.merge_range(row, 7, row + 4, 7, 'TP', format_header2_center)
        sheet.merge_range(row, 8, row + 4, 8, 'TE:', format_header2_center)
        sheet.merge_range(row, 9, row + 4, 9, 'Total:', format_header2_center)

        sheet.write(row, 10, 'Calificación', format_header2_center)
        row += 1
        sheet.write(row, 10, 'A – Excepcional', format_header2_center)
        row += 1
        sheet.write(row, 10, 'B – Aceptable', format_header2_center)
        row += 1
        sheet.write(row, 10, 'C – Aceptable con prueba adicional', format_header2_center)
        row += 1
        sheet.write(row, 10, 'D – Inaceptable', format_header2_center)

        sheet.set_column('B:B', 15)
        sheet.set_column('C:D', 30)
        sheet.set_column('E:J', 25)
        sheet.set_column('K:K', 38)
        sheet.set_column('L:L', 20)
        sheet.set_row(2, 35)

        row = 16
        record_count = 0

        if data.get('is_wizard'):
            records = self.env['res.partner.evaluation.history'].search([])

        filtered_records = records.filtered(lambda r: r.is_tyt_evaluation)
        if filtered_records:
            for record in filtered_records:
                record_count += 1
                sheet.write(row, 1, record_count, format_cell_left)
                sheet.write(row, 2, record.partner_id.name or '', format_cell_left)
                sheet.write(row, 3, '\n'.join(['- ' + x.name for x in record.partner_id.product_ids] or ''), format_cell_left)

                qualification_items = record.history_item_ids.mapped('qualification_item')
                column_start = 4
                for qualification_item in qualification_items:
                    sheet.write(row, column_start, qualification_item, format_cell_left)
                    column_start += 1

                sheet.write(row, 9, record.qualification, format_cell_left)
                evaluation_qualification = dict(record.partner_id._fields['evaluation_qualification']._description_selection(self.env)).get(record.partner_id.evaluation_qualification, '')
                sheet.write(row, 10, evaluation_qualification, format_cell_left)
                row += 1
