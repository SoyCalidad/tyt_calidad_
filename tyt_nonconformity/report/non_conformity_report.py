# -- coding: utf-8 --
from odoo import models
import xlsxwriter
import base64
import io
from PIL import Image
from datetime import datetime

class NonconformityReportMixin(models.AbstractModel):
    _name = 'report.tyt_nonconformity.nonconformity_report_mixin'
    _inherit = 'report.report_xlsx.abstract'

    def generate_nonconformity_report(self, workbook, data, nonconformities):
        sheet = workbook.add_worksheet("REGISTRO")

        # Add the company logo
        logo = self.env.company.logo
        if logo:
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
            'font_size': 9,
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
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })

        # Format for the "NO." column
        no_column_format = workbook.add_format({
            'bg_color': '#bfbfbf',
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })
        
        # Format for the "Indicaciones" title cell
        indications_title_format = workbook.add_format({
            'bold': True,
            'font_size': 10,
            'text_wrap': True
        })

        # Format for the indications text
        indications_format = workbook.add_format({
            'font_size': 8,
            'text_wrap': True
        })

        # Format for bold text within indications
        bold_format = workbook.add_format({
            'bold': True,
            'font_size': 8,
        })

        # Write the title
        sheet.merge_range('D3:G4', 'REGISTRO DE NO CONFORMIDAD', title_format)

        # Apply rich text formatting with specific words in bold
        sheet.write_rich_string('J5', 
            indications_title_format, "Indicaciones:", '\n',
            bold_format, "* ",indications_format, "Toda No Conformidad Debe ser redactada de manera correcta y la no conformidad indicar de manera más explícita el hallazgo (",
            bold_format, "Requisito:", indications_format, " 3.7.3. Entrega de resultados ",
            bold_format, "No Conformidad:", indications_format, " No se realiza envió de resultados mediante correo electrónico ",
            bold_format, "Evidencia que lo soporta:", indications_format, " Correo Electrónico Validando que se envié en la fecha indicada / ATI-04_Concentrado de control interno / ATI-01_Inventario de activos y componentes",
            indications_format
        )
        
        sheet.set_column('J:J', 78)
        
        # Headers
        headers = [
            'NO.',
            'FECHA',
            'PROCESO',
            'CLÁUSULA',
            'HALLAZGO',
            'DETALLE DEL HALLAZGO',
            'RETROALIMENTACIÓN'
        ]

        # Write the headers
        for col, header in enumerate(headers):
            sheet.write(7, col + 1, header, header_format)

        # Adjust the column widths
        sheet.set_column('A:A', 8.5)   # Para el logo
        sheet.set_column('B:B', 4.5)   # NO.
        sheet.set_column('C:C', 15)    # FECHA
        sheet.set_column('D:D', 15)    # PROCESO
        sheet.set_column('E:E', 25)    # CLÁUSULA
        sheet.set_column('F:F', 25)    # HALLAZGO
        sheet.set_column('G:G', 25)    # DETALLE DEL HALLAZGO
        sheet.set_column('H:H', 39)    # RETROALIMENTACIÓN

        # Set row 5 height to 60
        sheet.set_row(4, 60)

        # Fill the data
        for index, nonconformity in enumerate(nonconformities, start=1):
            row = 7 + index
            sheet.write(row, 1, index, no_column_format)
            sheet.write(row, 2, nonconformity.date_found.strftime('%Y-%m-%d') if nonconformity.date_found else '', data_format)
            sheet.write(row, 3, nonconformity.process_id.name, data_format)
            sheet.write(row, 4, ', '.join(req.name for req in nonconformity.iso_9001_requeriments_ids), data_format)
            sheet.write(row, 5, 'not implemented yet', data_format) # Hallazgo field not implemented yet
            sheet.write(row, 6, 'not implemented yet', data_format) # Detalle del hallazgo field not implemented yet
            sheet.write(row, 7, nonconformity.description or '', data_format)

class IndividualNonconformityReport(models.AbstractModel):
    _name = 'report.tyt_nonconformity.individual_nonconformity_report'
    _inherit = 'report.tyt_nonconformity.nonconformity_report_mixin'

    def generate_xlsx_report(self, workbook, data, nonconformities):
        self.generate_nonconformity_report(workbook, data, nonconformities)

class GeneralNonconformityReport(models.AbstractModel):
    _name = 'report.tyt_nonconformity.general_nonconformity_report'
    _inherit = 'report.tyt_nonconformity.nonconformity_report_mixin'

    def generate_xlsx_report(self, workbook, data, records):
        date_init = datetime.strptime(data['form']['date_init'], '%Y-%m-%d')
        date_fin = datetime.strptime(data['form']['date_fin'], '%Y-%m-%d')

        # Search for nonconformities within the date range
        nonconformities = self.env['mgmtsystem.nonconformity'].search([
            ('date_found', '>=', date_init),
            ('date_found', '<=', date_fin)
        ], order="date_found asc")

        # Call the mixin method with the filtered nonconformities
        self.generate_nonconformity_report(workbook, data, nonconformities)
