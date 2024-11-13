# -*- coding: utf-8 -*-
import base64
import io

from odoo import api, fields, models
from odoo.exceptions import UserError
from PIL import Image

class ReportMixin(models.AbstractModel):
    _name = 'report.matrix.mixin'

    def _get_workbook_formats(self, workbook):
        return {
            'header_blue': workbook.add_format({
                'font_size': 16,
                'bold': True,
                'bg_color': '#31879b',
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'subheader_blue': workbook.add_format({
                'font_size': 11,
                'bold': True,
                'bg_color': '#31879b',
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'text_wrap': True
            }),
            'subheader_blue_left': workbook.add_format({
                'font_size': 11, 
                'bold': True,
                'bg_color': '#31879b',
                'font_color': 'white',
                'align': 'left',
                'valign': 'vcenter',
                'border': 1,
                'text_wrap': True
            }),
            'format21_left': workbook.add_format({
                'font_size': 10,
                'align': 'left',
                'valign': 'vcenter',
                'border': 1,
                'text_wrap': True
            }),
            'format21_center': workbook.add_format({
                'font_size': 10,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'text_wrap': True
            }),
            'acciones_format': workbook.add_format({
                'font_size': 11, 
                'bold': True,
                'bg_color': '#31879b',
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'text_wrap': True
            }),
            'format21_center_11': workbook.add_format({
                'font_size': 11,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'text_wrap': True
            }),
            'format21_left_11': workbook.add_format({
                'font_size': 11,
                'align': 'left',
                'valign': 'vcenter',
                'border': 1,
                'text_wrap': True
            }),
            'format_gray': workbook.add_format({
                'font_size': 11,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'text_wrap': True,
                'bg_color': '#d8d8d8'
            }),
            'format_number': workbook.add_format({
                'font_size': 10,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'num_format': '0'
            })
        }

    def _write_header(self, sheet, formats, matrix):
        logo = matrix.company_id.logo or self.env.company.logo
        if logo:
            image_data = base64.b64decode(logo)
            image_stream = io.BytesIO(image_data)
            image = Image.open(image_stream)
            image_width, image_height = image.size
            aspect_ratio = image_height / image_width
            new_width = 130
            new_height = int(new_width * aspect_ratio)
            sheet.insert_image('A1', 'company_logo.png', {'image_data': image_stream, 'x_scale': new_width/image_width, 'y_scale': new_height/image_height, 'x_offset': 50})

        # Three empty rows before the title
        sheet.set_row(0, 20)
        sheet.set_row(1, 20)
        sheet.set_row(2, 20)

        # Main title (moved to columns F-K)
        sheet.merge_range('F4:K5', 'INVENTARIO DE LOS PRINCIPALES RIESGOS Y OPORTUNIDADES', formats['header_blue'])
        
        # Three empty rows after the title for spacing
        sheet.set_row(5, 20)
        sheet.set_row(6, 20)
        sheet.set_row(7, 20)
        
        sheet.set_row(8, 50)
        # Column headers (starting from column D)
        headers = [
            'No.', 'Parte interesada', 'Fuente del riesgo / oportunidad', 
            'Descripción del riesgo/oportunidad', 'R: Riesgo\nO: Oportunidad', 
            'Impacto', 'Probabilidad', 'Importancia', 
            'Acciones para abordar riesgos/oportunidades', 'Responsabilidad'
        ]
        
        for col, header in enumerate(headers, start=3):
            if header == 'Acciones para abordar riesgos/oportunidades':
                sheet.write(8, col, header, formats['acciones_format'])
            elif header == 'R: Riesgo\nO: Oportunidad':
                sheet.write(8, col, header, formats['subheader_blue_left'])
            else:
                sheet.write(8, col, header, formats['subheader_blue'])
            sheet.set_column(col, col, 15)  # Set column width

        # Adjust specific column widths
        sheet.set_column('D:D', 2.5)   # No.
        sheet.set_column('E:E', 12)  # Parte interesada
        sheet.set_column('F:F', 40)  # Fuente
        sheet.set_column('G:G', 40)  # Descripción
        sheet.set_column('L:L', 25)  # Acciones
        sheet.set_column('M:M', 15)  # Responsabilidad
    
    def _write_matrix_data(self, sheet, formats, matrix, workbook):
        row = 9
        for count, line in enumerate(matrix.line_ids, start=1):
            sheet.write(row, 3, count, formats['format_gray'])  # No.
            sheet.write(row, 4, line.stakeholder_id.name, formats['format21_center'])
            sheet.write(row, 5, line.risk_origin, formats['format21_center'])
            sheet.write(row, 6, line.description, formats['format21_center'])
            sheet.write(row, 7, 'R' if line.type == 'risk' else 'O', formats['format21_center'])
            
            if line.evaluation_id and line.evaluation_id.criterio_ids:
                impact_name = line.evaluation_id.criterio_ids[0].name
                probability_name = line.evaluation_id.criterio_ids[1].name if len(line.evaluation_id.criterio_ids) > 1 else ''
                
                impact_value = self._get_criterio_value(line, impact_name)
                probability_value = self._get_criterio_value(line, probability_name)
                
                # Convertir a entero y escribir como número
                sheet.write_number(row, 8, int(float(impact_value)) if impact_value else 0, formats['format_number'])
                sheet.write_number(row, 9, int(float(probability_value)) if probability_value else 0, formats['format_number'])
                
                # Escribir la fórmula para Importancia
                importance_formula = f'=SUM(I{row+1}:J{row+1})'
                sheet.write_formula(row, 10, importance_formula, formats['format_number'])
            else:
                sheet.write(row, 8, '', formats['format21_center'])
                sheet.write(row, 9, '', formats['format21_center'])
                sheet.write(row, 10, '', formats['format21_center'])
            
            actions = '\n'.join(x.name for x in line.action_ids)
            sheet.write(row, 11, actions, formats['format21_left_11'])  # Acciones
            if len(line.hr_job_id) > 1:
                responsible = ', '.join(x.name for x in line.hr_job_id)
            else:
                responsible = '\n'.join(x.name for x in line.hr_job_id)
            sheet.write(row, 12, responsible, formats['format21_center'])

            # Adjust row height to fit content
            sheet.set_row(row, None, None, {'level': 1, 'hidden': False})

            row += 1

        # Agregar formato condicional a la columna de Importancia
        sheet.conditional_format(9, 10, row - 1, 10, {
            'type': 'cell',
            'criteria': '>=',
            'value': 3,
            'format': workbook.add_format({
                'bg_color': '#ffc7ce',
                'font_color': '#9c0006',
                'num_format': '0'
            })
        })
        sheet.conditional_format(9, 10, row - 1, 10, {
            'type': 'cell',
            'criteria': '<',
            'value': 3,
            'format': workbook.add_format({
                'bg_color': '#c6efce',
                'font_color': '#006100',
                'num_format': '0'
            })
        })

    def _get_criterio_value(self, line, criterio_name):
        if not line.result_ids or not criterio_name:
            return ''
        
        result = line.result_ids.filtered(lambda r: r.criterio_id.name == criterio_name)
        if not result:
            return ''
        
        return result[0].value if result[0].value is not None else ''
    
class IndividualReport(models.AbstractModel):
    _name = 'report.mgmtsystem_opprisk.report'
    _inherit = ['report.report_xlsx.abstract', 'report.matrix.mixin']

    def generate_xlsx_report(self, workbook, data, matrixes):
        try:
            for matrix in matrixes:
                sheet = workbook.add_worksheet(str(matrix.name))
                formats = self._get_workbook_formats(workbook)
                self._write_header(sheet, formats, matrix)
                self._write_matrix_data(sheet, formats, matrix, workbook)
        except Exception as e:
            raise UserError(f"Error al generar el reporte: {str(e)}")

class MatrixReportXls(models.AbstractModel):
    _name = 'report.matrix_report_xls.xlsx'
    _inherit = ['report.report_xlsx.abstract', 'report.matrix.mixin']

    def generate_xlsx_report(self, workbook, data, lines):
        try:
            for matrix in lines.matrix_ids:
                sheet = workbook.add_worksheet(str(matrix.name))
                formats = self._get_workbook_formats(workbook)
                self._write_header(sheet, formats, matrix, lines.company_id.name)
                self._write_matrix_data(sheet, formats, matrix, workbook)
        except Exception as e:
            raise UserError(f"Error al generar el reporte: {str(e)}")
