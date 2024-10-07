# -- coding: utf-8 --
from odoo import models
import xlsxwriter
import base64
import io
from PIL import Image
from datetime import datetime

class ConformityEvaluationReportMixin(models.AbstractModel):
    _name = 'report.tyt_improve.conformity_evaluation_report_mixin'
    _inherit = 'report.report_xlsx.abstract'

    def generate_conformity_evaluation_report(self, workbook, data, evaluations):
        sheet = workbook.add_worksheet("REC")

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
            'font_size': 16,
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
            'font_size': 11,
            'font_color': 'white',
            'bg_color': '#31879b',
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
            'font_size': 11,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })
        
        # Write the title
        sheet.merge_range('D3:G4', 'REGISTRO DE EVALUACIÓN DE CONFORMIDAD', title_format)

        # New headers
        headers = [
            'No.',
            'Requerimiento de la parte interesada',
            'Conforme (Sí/No)',
            'Descripción de la no conformidad',
            'ID de la Acción Correctiva iniciada'
        ]

        # Write the new headers starting from C8
        for col, header in enumerate(headers):
            sheet.write(7, col + 2, header, header_format)

        # Adjust the column widths
        sheet.set_column('A:B', 10)    # Logo
        sheet.set_column('C:C', 4)     # NO.
        sheet.set_column('D:D', 34)    # Requerimiento de la parte interesada
        sheet.set_column('E:E', 17)    # Conforme (Sí/No)
        sheet.set_column('F:F', 31)    # Descripción de la no conformidad
        sheet.set_column('G:G', 31)    # ID de la Acción Correctiva iniciada

        # Fill the data
        for index, evaluation in enumerate(evaluations, start=1):
            row = 7 + index
            sheet.write(row, 2, index, no_column_format) # No.
            sheet.write(row, 3, evaluation.stakeholder_requirement or '', data_format) # Requerimiento de la parte interesada
            compliance_text = "Sí" if evaluation.compliance is True else "No" if evaluation.compliance is False else "-"
            sheet.write(row, 4, compliance_text, data_format) # Conforme (Sí/No)
            sheet.write(row, 5, evaluation.found_description or '', data_format) # Descripción de la No conformidad
            sheet.write(row, 6, evaluation.ref or '', data_format) # ID de la Acción Correctiva iniciada

class IndividualConformityEvaluationReport(models.AbstractModel):
    _name = 'report.tyt_improve.individual_conformity_evaluation_report'
    _inherit = 'report.tyt_improve.conformity_evaluation_report_mixin'

    def generate_xlsx_report(self, workbook, data, evaluations):
        self.generate_conformity_evaluation_report(workbook, data, evaluations)

class GeneralConformityEvaluationReport(models.AbstractModel):
    _name = 'report.tyt_improve.general_conformity_evaluation_report'
    _inherit = 'report.tyt_improve.conformity_evaluation_report_mixin'

    def generate_xlsx_report(self, workbook, data, records):
        date_init = datetime.strptime(data['form']['date_init'], '%Y-%m-%d')
        date_fin = datetime.strptime(data['form']['date_fin'], '%Y-%m-%d')

        # Search for evaluations within the date range
        evaluations = self.env['mgmtsystem.nonconformity'].search([
            ('date_found', '>=', date_init),
            ('date_found', '<=', date_fin)
        ], order="date_found asc")

        # Call the mixin method with the filtered evaluations
        self.generate_conformity_evaluation_report(workbook, data, evaluations)
