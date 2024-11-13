import base64
import io

from odoo import fields, models
from PIL import Image
from datetime import datetime

import io
import base64
from PIL import Image
from odoo.modules.module import get_module_resource


class CustomerDirectoryXlsxReport(models.AbstractModel):
    _name = 'report.customer_directory_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        white_bg_format = workbook.add_format({'bg_color': '#FFFFFF', 'border': 0})
        format_title = workbook.add_format(
            {'font_size': 30, 'color': '#FFFFFF', 'bg_color': '#215967', 'valign': 'vcenter', 'align': 'center',
             'bold': True, 'text_wrap': True, 'border': 2})
        format_header_left = workbook.add_format(
            {'font_size': 12, 'color': '#FFFFFF', 'bg_color': '#215967', 'valign': 'vcenter', 'align': 'left',
             'bold': True,
             'text_wrap': True, 'border': 2})
        format_cell_left = workbook.add_format(
            {'font_size': 11, 'align': 'left', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 1})

        sheet = workbook.add_worksheet('Directorio')
        sheet.set_column('A:XFD', None, white_bg_format)
        sheet.hide_gridlines(2)

        image_path = get_module_resource('tyt_contacts_reports', 'static/src/img', 'logo.png')
        with open(image_path, 'rb') as f:
            buf_image = io.BytesIO(f.read())
        im = Image.open(buf_image)
        width, height = im.size
        image_width = width
        image_height = height
        cell_width = 130
        cell_height = 104
        x_scale = cell_width / image_width
        y_scale = cell_height / image_height
        sheet.insert_image('B1:B3', "logo.png",
                           {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 10})

        sheet.merge_range(2, 3, 2, 7, 'DIRECTORIO CLIENTES', format_title)

        row = 7
        sheet.write(row, 1, 'PLAZA', format_header_left)
        sheet.write(row, 2, 'NOMBRE', format_header_left)
        sheet.write(row, 3, 'PUESTO', format_header_left)
        sheet.write(row, 4, 'CORREO', format_header_left)
        sheet.write(row, 5, 'TELEFONO', format_header_left)
        sheet.write(row, 6, 'CAMPAÑA', format_header_left)
        sheet.write(row, 7, 'EMPRESA', format_header_left)
        sheet.write(row, 8, 'OBSERVACIONES', format_header_left)
        sheet.write(row, 9, 'LIGA', format_header_left)

        sheet.set_column('B:B', 15)
        sheet.set_column('C:E', 30)
        sheet.set_column('F:G', 20)
        sheet.set_column('H:I', 30)
        sheet.set_column('J:J', 50)
        sheet.set_row(7, 30)

        if data.get('is_wizard'):
            domain = [('customer', '=', True)]
            if data.get('is_critical'):
                domain.append(('vip_customer', '=', True))
            records = self.env['res.partner'].search(domain, order='create_date desc')

        record_count = 0
        if records:
            for record in records:
                row += 1
                record_count += 1
                sheet.write(row, 1, record_count, format_cell_left)
                sheet.write(row, 2, record.name or '', format_cell_left)
                sheet.write(row, 3, record.function or '', format_cell_left)
                sheet.write(row, 4, record.email or '', format_cell_left)
                sheet.write(row, 5, record.phone or '', format_cell_left)
                sheet.write(row, 6, '\n'.join(['- ' + x.name for x in record.customer_campaign_ids] if record.customer else ''), format_cell_left)
                sheet.write(row, 7, record.parent_id.name or '', format_cell_left)
                sheet.write(row, 8, record.observations or '', format_cell_left)
                sheet.write(row, 9, record.website or '', format_cell_left)
