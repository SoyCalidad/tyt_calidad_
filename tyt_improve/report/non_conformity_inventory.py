# -- coding: utf-8 --
from odoo import models
import xlsxwriter
import base64
import io
from PIL import Image
from datetime import datetime
import html
import re

class NonconformityInventoryMixin(models.AbstractModel):
    _name = 'report.tyt_improve.nonconformity_inventory_mixin'
    _inherit = 'report.report_xlsx.abstract'

    def generate_nonconformity_report(self, workbook, data, nonconformities):
        sheet = workbook.add_worksheet("NO CONFORMIDADES")

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
            'font_size': 12,
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

        # Format for the "NO." column
        no_column_format = workbook.add_format({
            'bg_color': '#bfbfbf',
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })

        # Write the title
        sheet.merge_range('F3:H4', 'INVENTARIO DE NO CONFORMIDADES', title_format)

        # New Headers
        headers = [
            'No.',
            'Proceso',
            'Fecha de Auditoria',
            'Clausula/SubClausula',
            'Descripción de la No conformidad',
            'Breve descripción de la Acción Correctiva',
            'Fecha de Remediacion',
            'Estado de la AC',
            'Comentarios'
        ]

        # Write the headers
        for col, header in enumerate(headers):
            sheet.write(8, col + 1, header, header_format)

        # Adjust the column widths
        sheet.set_column('B:B', 4)   # No.
        sheet.set_column('C:C', 15)    # Proceso
        sheet.set_column('D:D', 17.70)    # Fecha de Auditoria
        sheet.set_column('E:E', 20.70)    # Clausula/SubClausula
        sheet.set_column('F:F', 32.20)    # Descripción de la No conformidad
        sheet.set_column('G:G', 39.30)    # Breve descripción de la Acción Correctiva
        sheet.set_column('H:H', 21.50)    # Fecha de Remediacion
        sheet.set_column('I:I', 14.90)    # Estado de la AC
        sheet.set_column('J:J', 24)    # Comentarios

        # Define state mapping
        state_mapping = {
            'open': 'Abierto',
            'follow': 'En seguimiento',
            'done': 'Cerrado',
            'cancel': 'Cancelado'
        }

        # Add data validation for the "Estado de la AC" column
        sheet.data_validation('I10:I1048576', {
            'validate': 'list',
            'source': list(state_mapping.values())
        })

        # Function to remove HTML tags
        def remove_html_tags(text):
            clean = re.compile('<.*?>')
            return re.sub(clean, '', text)

        # Fill the data
        row = 9  # Start from row 9 (as row 8 contains headers)
        for nonconformity in nonconformities:
            if nonconformity.action_ids:
                for action in nonconformity.action_ids:
                    sheet.write(row, 1, row - 8, no_column_format)
                    sheet.write(row, 2, nonconformity.process_id.name or '', data_format) # Proceso
                    sheet.write(row, 3, nonconformity.report_id.audit_id.date_init.strftime('%Y-%m-%d') if nonconformity.report_id.audit_id.date_init else '', data_format) # Fecha de Auditoria
                    sheet.write(row, 4, ', '.join(req.name for req in nonconformity.iso_9001_requeriments_ids), data_format)
                    sheet.write(row, 5, nonconformity.found_description or '', data_format) # Descripción de la No conformidad
                    sheet.write(row, 6, action.name or '', data_format) # Breve descripción de la Acción Correctiva
                    sheet.write(row, 7, action.date_deadline.strftime('%Y-%m-%d') if action.date_deadline else '', data_format) # Fecha de Remediacion
                    sheet.write(row, 8, state_mapping.get(action.state, ''), data_format) # Estado de la AC
                    sheet.write(row, 9, remove_html_tags(html.unescape(action.description or '')), data_format) # Comentarios
                    row += 1

class GeneralNonconformityReport(models.AbstractModel):
    _name = 'report.tyt_improve.general_nonconformity_inventory'
    _inherit = 'report.tyt_improve.nonconformity_inventory_mixin'

    def generate_xlsx_report(self, workbook, data, records):
        date_init = datetime.strptime(data['form']['date_init'], '%Y-%m-%d')
        date_fin = datetime.strptime(data['form']['date_fin'], '%Y-%m-%d')

        # Search for nonconformities within the date range using report_id.audit_id.date_init
        nonconformities = self.env['mgmtsystem.nonconformity'].search([
            ('report_id.audit_id.date_init', '>=', date_init),
            ('report_id.audit_id.date_init', '<=', date_fin)
        ], order="nc_create_date desc")

        # Call the mixin method with the filtered nonconformities
        self.generate_nonconformity_report(workbook, data, nonconformities)