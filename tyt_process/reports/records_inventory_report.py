# -- coding: utf-8 --
from odoo import models, fields
import xlsxwriter
import base64
import io
from PIL import Image
from datetime import datetime

class InventoryReportMixin(models.AbstractModel):
    _name = 'report.tyt_process.inventory_report_mixin'
    _inherit = 'report.report_xlsx.abstract'

    def generate_inventory_report(self, workbook, data, records, report_type):
        sheet = workbook.add_worksheet(f"INVENTARIO {report_type.upper()}")

        # Add the company logo
        logo = self.env.company.logo
        if (logo):
            image_data = base64.b64decode(logo)
            image_stream = io.BytesIO(image_data)
            image = Image.open(image_stream)
            image_width, image_height = image.size
            aspect_ratio = image_height / image_width
            new_width = 120
            new_height = int(new_width * aspect_ratio)
            sheet.insert_image('A1', 'company_logo.png', {
                'image_data': image_stream,
                'x_scale': new_width / image_width,
                'y_scale': new_height / image_height,
                'x_offset': 10
            })

        # Format for the main title
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'font_color': 'white',
            'bg_color': '#31879b',
            'align': 'center',
            'valign': 'vcenter',
            'border': 2,
            'border_color': '#757070',
        })

        # Format for the headers
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'font_color': 'white',
            'bg_color': '#286f80',
            'align': 'center',
            'valign': 'vcenter',
            'border': 2,
            'text_wrap': True,
            'border_color': '#757070',
        })

        # Format for the data
        data_format = workbook.add_format({
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })

        # Write the title
        sheet.merge_range('E3:G4', f'INVENTARIO {report_type.upper()}', title_format)

        # Headers
        headers = self.get_headers(report_type)

        # Write the headers
        for col, header in enumerate(headers, start=2):
            sheet.write(6, col, header, header_format)

        # Adjust the column widths
        self.set_column_widths(sheet)

        # Write data
        for row, record in enumerate(records, start=7):
            self.write_record_data(sheet, row, record, data_format, report_type)

    def get_headers(self, report_type):
        if report_type == 'EXTERNO':
            return [
                'No',
                'Número del Documento',
                'Remitente',
                'Nombre del Documento',
                'Fecha de recepción',
                'Persona que lo recibió'
            ]
        elif report_type == 'INTERNO':
            return [
                'No',
                'Número del Documento',
                'Destinatario',
                'Nombre del Documento',
                'Fecha de envío',
                'Persona que lo envió'
            ]
        elif report_type == 'DE REGISTROS':
            return [
                'No',
                'Número del Documento',
                'Remitente',
                'Nombre del Documento',
                'Fecha de recepción',
                'Persona'
            ]

    def set_column_widths(self, sheet):
        sheet.set_column('C:C', 5)   # No
        sheet.set_column('D:D', 30)  # Número del Documento
        sheet.set_column('E:E', 13)  # Remitente/Destinatario
        sheet.set_column('F:F', 30)  # Nombre del Documento
        sheet.set_column('G:G', 24)  # Fecha de recepción/envío
        sheet.set_column('H:H', 27)  # Persona que lo recibió/envió

    def write_record_data(self, sheet, row, record, data_format, report_type):
        sheet.write(row, 2, row - 6, data_format) # No
        sheet.write(row, 3, record.code or '', data_format) # Número del Documento
        sheet.write(row, 4, record.sender_id.name or '', data_format) # Remitente/Destinatario
        sheet.write(row, 5, record.name or '', data_format) # Nombre del Documento
        sheet.write(row, 6, record.reception_date.strftime('%d/%m/%Y') if record.reception_date else '', data_format) # Fecha de recepción/envío
        sheet.write(row, 7, record.received_by_id.name or '', data_format) # Persona que lo recibió/envió

class WizardExternalInventoryReport(models.AbstractModel):
    _name = 'report.tyt_process.wizard_external_inventory'
    _inherit = 'report.tyt_process.inventory_report_mixin'

    def generate_xlsx_report(self, workbook, data, records):
        date_init = datetime.strptime(data['form']['date_init'], '%Y-%m-%d')
        date_fin = datetime.strptime(data['form']['date_fin'], '%Y-%m-%d')

        documentary_control = self.env['documentary.control']
        external_records = documentary_control.search([
            ('type', '=', 'externa'),
            ('reception_date', '>=', date_init),
            ('reception_date', '<=', date_fin)
        ], order="reception_date desc")

        self.generate_inventory_report(workbook, data, external_records, 'EXTERNO')

class WizardlInternalInventoryReport(models.AbstractModel):
    _name = 'report.tyt_process.wizard_internal_inventory'
    _inherit = 'report.tyt_process.inventory_report_mixin'

    def generate_xlsx_report(self, workbook, data, records):
        date_init = datetime.strptime(data['form']['date_init'], '%Y-%m-%d')
        date_fin = datetime.strptime(data['form']['date_fin'], '%Y-%m-%d')

        documentary_control = self.env['documentary.control']
        internal_records = documentary_control.search([
            ('type', '=', 'interna'),
            ('reception_date', '>=', date_init),
            ('reception_date', '<=', date_fin)
        ], order="reception_date desc")

        self.generate_inventory_report(workbook, data, internal_records, 'INTERNO')

class GeneralInventoryReport(models.AbstractModel):
    _name = 'report.tyt_process.general_inventory'
    _inherit = 'report.tyt_process.inventory_report_mixin'

    def generate_xlsx_report(self, workbook, data, records):
        
        self.generate_inventory_report(workbook, data, records, 'DE REGISTROS')