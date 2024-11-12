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
        format_header_center = workbook.add_format(
            {'font_size': 11, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vcenter', 'align': 'center',
             'bold': True,
             'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_cell_left = workbook.add_format(
            {'font_size': 11, 'align': 'left', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 2, 'border_color': '#808080'})
        format_cell_right = workbook.add_format(
            {'font_size': 11, 'align': 'right', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 2,
             'border_color': '#808080'})
        format_monetary = workbook.add_format(
            {'num_format': '#,##0.00', 'font_size': 11, 'align': 'right',
             'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 1})

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
        cell_width = 110
        cell_height = 64
        x_scale = cell_width / image_width
        y_scale = cell_height / image_height
        sheet.insert_image('B1:B3', "logo.png",
                           {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 10})

        sheet.merge_range(2, 3, 2, 7, 'LISTA DE PROVEEDORES APROBADOS', format_title)

        row = 7
        sheet.write(row, 1, 'NO.', format_header_center)
        sheet.write(row, 2, 'PROVEEDOR', format_header_center)
        sheet.write(row, 3, 'BIENES/SERVICIO', format_header_center)
        sheet.write(row, 4, 'FECHA DE EVALUACIÓN', format_header_center)
        sheet.write(row, 5, 'CALIFICACIÓN', format_header_center)
        sheet.write(row, 6, 'FECHA DE EVALUACIÓN', format_header_center)
        sheet.write(row, 7, 'CALIFICACIÓN', format_header_center)
        sheet.write(row, 8, 'NOTA', format_header_center)

        sheet.set_column('B:I', 20)
        sheet.set_column('C:D', 35)
        sheet.set_column('E:I', 25)
        sheet.set_row(7, 24)

        if data.get('is_wizard'):
            domain = [('supplier', '=', True)]
            if data.get('is_critical'):
                domain.append(('vip_supplier', '=', True))
            records = self.env['res.partner'].search(domain, order='create_date desc')

        row = 8
        record_count = 0
        if records:
            for record in records:
                record_count += 1
                sheet.write(row, 1, record_count, format_cell_left)
                sheet.write(row, 2, record.name, format_cell_left)
                sheet.write(row, 3, '\n'.join(['- ' + x.name for x in record.product_ids] or ''), format_cell_left)

                total_qualification = 0
                history_count = 0
                for index, history in enumerate(record.history_ids[:2]):
                    sheet.write(row, 4 + index * 2, history.date_history.strftime('%d/%m/%Y %H:%M:%S') if history.date_history else '', format_cell_left)
                    evaluation_qualification = dict(
                        history._fields['evaluation_qualification']._description_selection(self.env)).get(
                        history.evaluation_qualification, '')
                    sheet.write(row, 5 + index * 2, evaluation_qualification, format_cell_left)

                    if history.qualification:
                        total_qualification += history.qualification
                        history_count += 1

                average_qualification = total_qualification / history_count if history_count > 0 else 0.00
                sheet.write(row, 8, average_qualification, format_monetary)
                row += 1
