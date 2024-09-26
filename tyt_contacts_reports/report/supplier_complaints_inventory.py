from odoo import fields, models
import io
from PIL import Image
from odoo.modules.module import get_module_resource


class SupplierComplaintsInventoryXlsxReport(models.AbstractModel):
    _name = 'report.supplier_complaints_inventory_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        white_bg_format = workbook.add_format({'bg_color': '#FFFFFF', 'border': 0})
        format_title = workbook.add_format({'font_size': 22, 'color': '#FFFFFF', 'bg_color': '#31869B', 'valign': 'vbottom', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 2})
        format_header_left = workbook.add_format({'font_size': 11, 'bg_color': '#B7DEE8', 'valign': 'vcenter', 'align': 'left', 'bold': True, 'text_wrap': True, 'border': 2})
        format_cell_left = workbook.add_format({'font_size': 11, 'align': 'left', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 2})

        sheet = workbook.add_worksheet('Inventario')
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
        cell_height = 144
        x_scale = cell_width / image_width
        y_scale = cell_height / image_height
        sheet.insert_image('B1:B3', "logo.png",
                           {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 10})

        sheet.merge_range(2, 3, 2, 7, 'INVENTARIO DE RECLAMOS SOBRE PROVEEDORES', format_title)

        row = 9
        sheet.write(row, 1, 'No.', format_header_left)
        sheet.write(row, 2, 'Fecha de envío', format_header_left)
        sheet.write(row, 3, 'Producto/Nombre del servicio', format_header_left)
        sheet.write(row, 4, 'Proveedor', format_header_left)
        sheet.write(row, 5, 'Descripción del reclamo', format_header_left)
        sheet.write(row, 6, 'Documento de referencia', format_header_left)
        sheet.write(row, 7, 'Fecha de resolución del reclamo', format_header_left)
        sheet.write(row, 8, 'Registrado por', format_header_left)

        sheet.set_column('B:I', 25)
        sheet.set_column('D:E', 30)
        sheet.set_column('F:F', 30)
        sheet.set_column('H:H', 30)
        sheet.set_row(2, 35)
        sheet.set_row(3, 25)

        if data.get('is_wizard'):
            date_from = data.get('date_from')
            date_to = data.get('date_to')
            records = self.env['supplier_complaints_inventory'].search([
                ('shipment_date', '>=', date_from),
                ('shipment_date', '<=', date_to)
            ], order='create_date desc')

        record_count = 0
        if records:
            for record in records:
                row += 1
                record_count += 1
                sheet.write(row, 1, record_count, format_cell_left)
                sheet.write(row, 2, record.shipment_date.strftime('%d/%m/%Y') if record.shipment_date else '', format_cell_left)
                sheet.write(row, 3, record.product_service or '', format_cell_left)
                sheet.write(row, 4, record.supplier_id.name or '', format_cell_left)
                sheet.write(row, 5, record.description or '', format_cell_left)
                sheet.write(row, 6, record.document_reference or '', format_cell_left)
                sheet.write(row, 7, record.resolution_date.strftime('%d/%m/%Y') if record.resolution_date else '', format_cell_left)
                sheet.write(row, 8, record.register_id.name or '', format_cell_left)
