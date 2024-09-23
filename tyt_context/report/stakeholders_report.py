# -*- coding: utf-8 -*-
from odoo import models
import xlsxwriter
import base64
import io
from PIL import Image

class StakeholdersReportMixin(models.AbstractModel):
    _name = 'report.tyt_context.stakeholders_report_mixin'
    _inherit = 'report.report_xlsx.abstract'

    def generate_stakeholders_report(self, workbook, data, stakeholders):
        # Maintain a set of used sheet names to ensure uniqueness
        used_sheet_names = set()

        for stakeholder in stakeholders:      
            # Create a safe sheet name
            sheet_name = stakeholder.name[:31]  # Excel sheet name has a maximum of 31 characters
            # Remove invalid characters
            sheet_name = ''.join([c for c in sheet_name if c not in ('\\', '/', '*', '[', ']', ':', '?')])
            # Ensure the sheet name is unique
            original_sheet_name = sheet_name
            idx = 1
            while sheet_name in used_sheet_names:
                # If the name is already used, add a numeric suffix
                suffix = ' ({})'.format(idx)
                sheet_name = original_sheet_name[:31 - len(suffix)] + suffix
                idx += 1
            used_sheet_names.add(sheet_name)

            # Create the sheet with the stakeholder's name
            sheet = workbook.add_worksheet(sheet_name)
            # Freeze the first 8 rows and the first 2 columns
            sheet.freeze_panes(8, 2)
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

            # Write the title
            sheet.merge_range('D2:G3', 'PARTES INTERESADAS AUTORIDADES', title_format)

            # Headers
            headers = [
                'No.',
                'Parte interesada',
                'Necesidades y expectativas de las partes interesadas',
                'Documento que estipula la necesidad / obligación de cumplimiento',
                'Objetivo de la Necesidad',
                'Procedimiento/proceso/ actividad relacionado',
                'Puesto responsable',
                'Fecha límite para cumplir con el requisito',
                'Poder',
                'Interés',
                'Nivel de pertenencia'
            ]

            # Write the headers
            for col, header in enumerate(headers):
                sheet.write(7, col + 1, header, header_format)

            # Adjust the column widths
            sheet.set_column('A:A', 8.5)   # Para el logo
            sheet.set_column('B:B', 8.5)   # No.
            sheet.set_column('C:C', 25)    # Parte interesada
            sheet.set_column('D:D', 45)    # Necesidades y expectativas
            sheet.set_column('E:E', 25)    # Documento que estipula
            sheet.set_column('F:F', 70)    # Objetivo de la Necesidad
            sheet.set_column('G:G', 65)    # Procedimiento/proceso
            sheet.set_column('H:H', 25)    # Puesto responsable
            sheet.set_column('I:I', 25)    # Fecha límite
            sheet.set_column('J:J', 15)    # Poder
            sheet.set_column('K:K', 15)    # Interés
            sheet.set_column('L:L', 15)    # Nivel de pertenencia

            # Adjust the row heights
            sheet.set_row(7, 30)

            # Fill the data
            row = 8
            contador = 1
            for req in stakeholder.requirements:
                sheet.write(row, 1, contador, data_format)  # No.
                sheet.write(row, 2, stakeholder.name, data_format)  # Parte interesada
                sheet.write(row, 3, req.name, data_format)  # Necesidades y expectativas
                sheet.write(row, 4, req.legal_id.name if req.is_legal else '', data_format)  # Documento que estipula
                sheet.write(row, 5, req.target_req if req.target_req else '', data_format) # Objetivo de la Necesidad
                sheet.write(row, 6, '', data_format) # Procedimiento/proceso relacionado (Aún no se implementa)
                sheet.write(row, 7, req.job_req.name if req.job_req else '', data_format)  # Puesto responsable
                sheet.write(row, 8, req.limit_date_req if req.limit_date_req else '', data_format)  # Fecha límite
                sheet.write(row, 9, 'Menor' if stakeholder.power == '1' else 'Mayor' if stakeholder.power == '2' else '', data_format)  # Poder
                sheet.write(row, 10, 'Menor' if stakeholder.interest == '1' else 'Mayor' if stakeholder.interest == '2' else '', data_format)  # Interés
                sheet.write(row, 11, stakeholder.membership if stakeholder.membership else '', data_format)  # Nivel de pertenencia

                row += 1
                contador += 1

class IndividualStakeholdersReport(models.AbstractModel):
    _name = 'report.tyt_context.individual_stakeholders_report'
    _inherit = 'report.tyt_context.stakeholders_report_mixin'

    def generate_xlsx_report(self, workbook, data, stakeholders):
        # For the individual report, we use the provided stakeholders
        # Normally stakeholders will contain a single element
        self.generate_stakeholders_report(workbook, data, stakeholders)

class GeneralStakeholdersReport(models.AbstractModel):
    _name = 'report.tyt_context.general_stakeholders_report'
    _inherit = 'report.tyt_context.stakeholders_report_mixin'

    def generate_xlsx_report(self, workbook, data, partners):
        # For the general report, we get the stakeholders from the 'stakeholder_in_ids' and 'stakeholder_out_ids' fields
        stakeholders_in = partners.mapped('stakeholder_in_ids')
        stakeholders_out = partners.mapped('stakeholder_out_ids')
        stakeholders = stakeholders_in | stakeholders_out

        # Call the mixin method with the combined stakeholders
        self.generate_stakeholders_report(workbook, data, stakeholders)
