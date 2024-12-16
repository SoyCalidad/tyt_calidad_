# -*- coding: utf-8 -*-
import base64
import io
from datetime import date, datetime
from math import ceil
from collections import defaultdict

from odoo import api, fields, models
from odoo.exceptions import UserError
from PIL import Image

class ReportMixin(models.AbstractModel):
    _name = 'report.tyt_mgmt_review.report.mixin'
    _description = 'Mixin for Management Review Plan Reports'
    _inherit = 'report.report_xlsx.abstract'

    def _get_workbook_formats(self, workbook):
        formats = {
            'header_large': workbook.add_format({
                'font_size': 22,
                'bold': True,
                'bg_color': '#215967',
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 2
            }),
            'header_small': workbook.add_format({
                'font_size': 13,
                'bold': True,
                'bg_color': '#215967',
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 2,
                'text_wrap': True
            }),
            'cell': workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'border': 2,
                'text_wrap': True
            }),
            'cell_no_border': workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'text_wrap': True
            }),
            'percentage': workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'border': 2,
                'num_format': '0%'
            }),
            'border_2': workbook.add_format({
                'border': 2
            }),
            'border_1': workbook.add_format({
                'border': 1
            }),
            'cumplimiento_auditorias': workbook.add_format({
                'font_size': 22,
                'bold': True,
                'bg_color': '#31869b',
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 2
            }),
            'general_nacional_header': workbook.add_format({
                'font_size': 13,
                'bold': True,
                'bg_color': '#215967',
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 2,
                'text_wrap': True
            }),
            'general_nacional_value': workbook.add_format({
                'font_size': 14,
                'bg_color': '#d8d8d8',
                'font_color': 'black',
                'align': 'center',
                'valign': 'vcenter',
                'bold': True,
                'border': 2,
                'num_format': '0.00%',
                'text_wrap': True
            }),
            'general_sitios_value': workbook.add_format({
                'font_size': 14,
                'bg_color': '#d8d8d8',
                'font_color': 'black',
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'border': 2,
                'num_format': '0.00%',
                'text_wrap': True
            }),
            'cell_gray': workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'bold': True,
                'border': 2,
                'text_wrap': True,
                'bg_color': '#bfbfbf'
            }),
            'red_bold_percentage': workbook.add_format({
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter',
                'border': 2,
                'text_wrap': True,
                'font_color': '#c40000',
                'bold': True,
                'num_format': '0%'
            }),
            'black_bold_percentage': workbook.add_format({
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter',
                'border': 2,
                'text_wrap': True,
                'font_color': 'black',
                'bold': True,
                'num_format': '0%'
            }),
            'cell_size_12': workbook.add_format({
                'font_size': 12,
                'align': 'center',
                'valign': 'vcenter',
                'border': 2,
                'text_wrap': True
            }),
            'percentage_size_12': workbook.add_format({
                'font_size': 12,
                'align': 'center',
                'valign': 'vcenter',
                'border': 2,
                'num_format': '0%'
            }),
        }
        return formats

    def _insert_logo(self, sheet, workbook, actions):
        logo = actions.company_id.logo or self.env.company.logo
        if logo:
            image_data = base64.b64decode(logo)
            image_stream = io.BytesIO(image_data)
            image = Image.open(image_stream)
            image_width, image_height = image.size
            aspect_ratio = image_height / image_width
            new_width = 120
            new_height = int(new_width * aspect_ratio)
            sheet.insert_image('B1', 'company_logo.png', {'image_data': image_stream, 'x_scale': new_width/image_width, 'y_scale': new_height/image_height, 'x_offset': 50})

class GeneralReport(models.AbstractModel):
    _name = 'report.tyt_mgmt_review.general_report'
    _description = 'Reporte de Revisión por la Dirección'
    _inherit = 'report.tyt_mgmt_review.report.mixin'

    def generate_xlsx_report(self, workbook, data, actions):
        formats = self._get_workbook_formats(workbook)
        
        # Create the main worksheet named "General"
        main_sheet = workbook.add_worksheet('General')
        self._insert_logo(main_sheet, workbook, actions)
        self._write_general_sheet(main_sheet, formats, actions)
        
        # Create additional worksheets for each line
        for line in actions.line_ids:
            sheet_name = line.location_id.name if line.location_id else f"Revisión {line.name}"
            sheet = workbook.add_worksheet(sheet_name)
            self._insert_logo(sheet, workbook, actions)
            self._write_line_sheet(sheet, formats, line)

    def _write_general_sheet(self, sheet, formats, actions):
        sheet.merge_range('D2:G3', 'CUMPLIMIENTO GENERAL', formats['header_large'])
        
        headers = ['ÁREA RESPONSABLE DE CLAUSULA', 'TOTAL', 'BUENAS PRACTICAS', 'NO CONFORMIDADES', '% CUMPLIMIENTO', '% NO CUMPLIMIENTO']
        for col, header in enumerate(headers):
            sheet.write(7, col + 1, header, formats['header_small'])
        
        # Set column widths
        sheet.set_column('B:B', 30) # ÁREA RESPONSABLE DE CLAUSULA
        sheet.set_column('C:D', 15)  # TOTAL, BUENAS PRACTICAS
        sheet.set_column('E:E', 20)  # NO CONFORMIDADES
        sheet.set_column('F:G', 20) # % CUMPLIMIENTO, % NO CUMPLIMIENTO
        
        area_data, plaza_data = self._gather_data(actions)
        last_area_row = self._fill_general_data(sheet, formats, area_data, plaza_data, actions)
        
        sheet.set_column('I:I', 15)  # GENERAL NACIONAL and GENERAL NACIONAL ÁREA
        sheet.set_column('J:J', 13) # GENERAL NACIONAL value
        # Calculate GENERAL NACIONAL
        sheet.write('I6', 'GENERAL NACIONAL', formats['general_nacional_header'])
        sheet.write_formula('J6', f'=AVERAGE(F9:F{last_area_row-1})', formats['general_nacional_value'])
        
        # Calculate GENERAL NACIONAL ÁREA
        num_plazas = len(plaza_data)
        general_sitios_col = chr(67 + len(area_data) + 1)
        general_sitios_start_row = last_area_row + 5  # 4 rows for spacing and headers
        general_sitios_end_row = general_sitios_start_row + num_plazas - 1
        
        sheet.write(last_area_row + 1, 8, 'GENERAL NACIONAL ÁREA', formats['general_nacional_header'])
        sheet.write_formula(last_area_row + 1, 9, 
                            f'=AVERAGE({general_sitios_col}{general_sitios_start_row}:{general_sitios_col}{general_sitios_end_row})', 
                            formats['general_nacional_value'])

        # Apply border 2 to all cells in the General sheet
        sheet.conditional_format(0, 0, sheet.dim_rowmax, sheet.dim_colmax, {'type': 'no_blanks', 'format': formats['border_2']})

    def _gather_data(self, actions):
        area_data = defaultdict(lambda: {'total': 0, 'good': 0, 'bad': 0})
        plaza_data = defaultdict(lambda: defaultdict(int))
        
        for line in actions.line_ids:
            for line2 in line.line2_ids:
                area = line2.department_clau_id.name
                
                area_data[area]['total'] += 1
                if line2.achieved:
                    area_data[area]['good'] += 1
                else:
                    area_data[area]['bad'] += 1
                
                plaza = line.location_id.name
                if line2.achieved:
                    plaza_data[plaza][area] += 1
        
        return area_data, plaza_data

    def _fill_general_data(self, sheet, formats, area_data, plaza_data, actions):
        row = 8
        for area, data in area_data.items():
            sheet.write(row, 1, area, formats['cell_gray'])
            
            # Formulas for "BUENAS PRACTICAS" and "NO CONFORMIDADES"
            good_formula = '+'.join([
                f"IFERROR(VLOOKUP(\"{area}\", {line.location_id.name}!K:M, 2, FALSE), 0)"
                for line in actions.line_ids if line.location_id
            ])
            bad_formula = '+'.join([
                f"IFERROR(VLOOKUP(\"{area}\", {line.location_id.name}!K:M, 3, FALSE), 0)"
                for line in actions.line_ids if line.location_id
            ])
            
            sheet.write_formula(row, 2, f'=SUM(D{row+1}:E{row+1})', formats['cell_size_12'])
            sheet.write_formula(row, 3, good_formula, formats['cell_size_12'])
            sheet.write_formula(row, 4, bad_formula, formats['cell_size_12'])
            sheet.write_formula(row, 5, f'=D{row+1}/C{row+1}', formats['black_bold_percentage'])
            sheet.write_formula(row, 6, f'=E{row+1}/C{row+1}', formats['red_bold_percentage'])
            row += 1
        
        # Add an empty row without borders
        for col in range(1, 7):
            sheet.write(row, col, '', formats['cell_no_border'])
        
        last_area_row = row + 1
        
        # Plaza table
        row += 4  # Add an extra row here
        headers = ['PLAZA'] + list(area_data.keys()) + ['GENERAL SITIOS']
        sheet.set_column('H:H', 15)  # GENERAL SITIOS
        
        for col, header in enumerate(headers):
            sheet.write(row, col + 2, header, formats['header_small'])
        
        row += 1
        for plaza, areas in plaza_data.items():
            sheet.write(row, 2, plaza, formats['cell_gray'])
            for col, area in enumerate(area_data.keys(), start=3):
                sheet.write_formula(row, col, 
                    f'=IFERROR(INDEX({plaza}!O:O, MATCH("{area}", {plaza}!K:K, 0)), 0)', 
                    formats['percentage_size_12'])
            sheet.write_formula(row, len(headers) + 1, f'=AVERAGE(D{row+1}:{chr(67+len(area_data))}{row+1})', formats['general_sitios_value'])
            row += 1
        
        return last_area_row

    def _write_line_sheet(self, sheet, formats, line):
        sheet.merge_range('D2:G3', 'CUMPLIMIENTO DE AUDITORIAS', formats['cumplimiento_auditorias'])
        
        headers = [
            'NOMBRE', 'PUESTO', 'CLAUSULA', 'DESCRIPCIÓN', 'PROCESOS',
            'ÁREA RESPONSABLE PROCESO', 'ÁREA RESPONSABLE DE CLAUSULA', 'CUMPLE'
        ]
        
        # Aplicar borde 2 a la tabla principal
        sheet.conditional_format(9, 1, 9 + len(line.line2_ids), len(headers), {'type': 'no_blanks', 'format': formats['border_2']})
        
        for col, header in enumerate(headers):
            sheet.write(9, col + 1, header, formats['header_small'])
            sheet.set_column(col + 1, col + 1, 15)

        sheet.set_column('B:B', 35) # NOMBRE
        sheet.set_column('C:C', 45) # PUESTO
        sheet.set_column('D:D', 40) # CLAUSULA
        sheet.set_column('E:E', 65) # DESCRIPCIÓN
        sheet.set_column('F:F', 45) # PROCESOS
        sheet.set_column('G:G', 30) # ÁREA RESPONSABLE PROCESO
        sheet.set_column('H:H', 30) # ÁREA RESPONSABLE DE CLAUSULA
        sheet.set_column('I:I', 15) # CUMPLE

        row = 10
        for line2 in line.line2_ids:
            col = 1
            sheet.write(row, col, line2.name.name if line2.name else '', formats['cell'])
            sheet.write(row, col + 1, line2.name.job_id.name if line2.name and line2.name.job_id else '', formats['cell'])
            sheet.write(row, col + 2, line2.clausule_id.name if line2.clausule_id else '', formats['cell'])
            sheet.write(row, col + 3, line2.description if line2.description else '', formats['cell'])
            sheet.write(row, col + 4, line2.process2_id.name if line2.process2_id else '', formats['cell'])
            sheet.write(row, col + 5, line2.department_pro_id.name if line2.department_pro_id else '', formats['cell'])
            sheet.write(row, col + 6, line2.department_clau_id.name if line2.department_clau_id else '', formats['cell'])
            sheet.write(row, col + 7, 'Si' if line2.achieved else 'No', formats['cell'])
            row += 1

        last_row = row - 1
        total_entries = last_row - 10 + 1  # Total number of entries

        summary_headers = ['ÁREA RESPONSABLE DE CLAUSULA', 'Cumple', 'No Cumple', 'TOTAL', '% Cumple', '% No Cumple']
        
        # Aplicar borde 1 a la tabla de resumen
        sheet.conditional_format(9, 10, 9 + len(set(line2.department_clau_id.name for line2 in line.line2_ids if line2.department_clau_id)), 15, {'type': 'no_blanks', 'format': formats['border_1']})
        
        for col, header in enumerate(summary_headers):
            sheet.write(9, col + 10, header, formats['header_small'])

        sheet.set_column('K:K', 30)  # ÁREA RESPONSABLE DE CLAUSULA
        sheet.set_column('L:L', 8)   # Cumple
        sheet.set_column('M:M', 9.5) # No Cumple
        sheet.set_column('N:N', 8.5) # TOTAL
        sheet.set_column('O:O', 11.5)# % Cumple
        sheet.set_column('P:P', 11.5)# % No Cumple

        unique_areas = set(line2.department_clau_id.name for line2 in line.line2_ids if line2.department_clau_id)

        summary_row = 10
        for area in unique_areas:
            sheet.write(summary_row, 10, area, formats['cell'])
            sheet.write_formula(summary_row, 11, f'=COUNTIFS($H$11:$H${10+total_entries},$K{summary_row+1},$I$11:$I${10+total_entries},"Si")', formats['cell'])
            sheet.write_formula(summary_row, 12, f'=COUNTIFS($H$11:$H${10+total_entries},$K{summary_row+1},$I$11:$I${10+total_entries},"No")', formats['cell'])
            sheet.write_formula(summary_row, 13, f'=SUM(L{summary_row+1}:M{summary_row+1})', formats['cell'])
            sheet.write_formula(summary_row, 14, f'=L{summary_row+1}/N{summary_row+1}', formats['percentage'])
            sheet.write_formula(summary_row, 15, f'=M{summary_row+1}/N{summary_row+1}', formats['percentage'])
            summary_row += 1

class IndividualReport(models.AbstractModel):
    _name = 'report.tyt_mgmt_review.individual_report'
    _description = 'Revisión por la Dirección'
    _inherit = 'report.tyt_mgmt_review.report.mixin'

    def generate_xlsx_report(self, workbook, data, actions):
        formats = self._get_workbook_formats(workbook)
        for action in actions:
            sheet_name = action.location_id.name if action.location_id else f"Revisión {action.name}"
            sheet = workbook.add_worksheet(sheet_name[:31])
            self._insert_logo(sheet, workbook, action)
            self._write_individual_sheet(sheet, formats, action)

    def _write_individual_sheet(self, sheet, formats, actions):
        sheet.merge_range('D2:G3', 'CUMPLIMIENTO DE AUDITORIAS', formats['cumplimiento_auditorias'])
        
        headers = [
            'NOMBRE', 'PUESTO', 'CLAUSULA', 'DESCRIPCIÓN', 'PROCESOS',
            'ÁREA RESPONSABLE PROCESO', 'ÁREA RESPONSABLE DE CLAUSULA', 'CUMPLE'
        ]
        
        for col, header in enumerate(headers):
            sheet.write(8, col + 1, header, formats['header_small'])

        # Set column widths
        sheet.set_column('B:B', 35) # NOMBRE
        sheet.set_column('C:C', 45) # PUESTO
        sheet.set_column('D:D', 40) # CLAUSULA
        sheet.set_column('E:E', 65) # DESCRIPCIÓN
        sheet.set_column('F:F', 45) # PROCESOS
        sheet.set_column('G:G', 30) # ÁREA RESPONSABLE PROCESO
        sheet.set_column('H:H', 30) # ÁREA RESPONSABLE DE CLAUSULA
        sheet.set_column('I:I', 15) # CUMPLE

        row = 9
        for line2 in actions.line2_ids:
            col = 1
            sheet.write(row, col, line2.name.name if line2.name else '', formats['cell'])
            sheet.write(row, col + 1, line2.name.job_id.name if line2.name and line2.name.job_id else '', formats['cell'])
            sheet.write(row, col + 2, line2.clausule_id.name if line2.clausule_id else '', formats['cell'])
            sheet.write(row, col + 3, line2.description if line2.description else '', formats['cell'])
            sheet.write(row, col + 4, line2.process2_id.name if line2.process2_id else '', formats['cell'])
            sheet.write(row, col + 5, line2.department_pro_id.name if line2.department_pro_id else '', formats['cell'])
            sheet.write(row, col + 6, line2.department_clau_id.name if line2.department_clau_id else '', formats['cell'])
            sheet.write(row, col + 7, 'Si' if line2.achieved else 'No', formats['cell'])
            row += 1

        last_row = row - 1
        total_entries = last_row - 9  # Total number of entries

        # Apply border 2 to the main table
        sheet.conditional_format(9, 1, last_row, len(headers), {'type': 'no_blanks', 'format': formats['border_2']})

        # Summary table
        summary_headers = ['ÁREA RESPONSABLE DE CLAUSULA', 'Cumple', 'No Cumple', 'TOTAL', '% Cumple', '% No Cumple']
        
        for col, header in enumerate(summary_headers):
            sheet.write(9, col + 10, header, formats['header_small'])

        sheet.set_column('K:K', 30)  # ÁREA RESPONSABLE DE CLAUSULA
        sheet.set_column('L:L', 8)   # Cumple
        sheet.set_column('M:M', 9.5) # No Cumple
        sheet.set_column('N:N', 8.5) # TOTAL
        sheet.set_column('O:O', 11.5)# % Cumple
        sheet.set_column('P:P', 11.5)# % No Cumple

        unique_areas = set(line2.department_clau_id.name for line2 in actions.line2_ids if line2.department_clau_id)

        summary_row = 10
        for area in unique_areas:
            sheet.write(summary_row, 10, area, formats['cell'])
            sheet.write_formula(summary_row, 11, f'=COUNTIFS($H$10:$H${10+total_entries},$K{summary_row+1},$I$10:$I${10+total_entries},"Si")', formats['cell'])
            sheet.write_formula(summary_row, 12, f'=COUNTIFS($H$10:$H${10+total_entries},$K{summary_row+1},$I$10:$I${10+total_entries},"No")', formats['cell'])
            sheet.write_formula(summary_row, 13, f'=SUM(L{summary_row+1}:M{summary_row+1})', formats['cell'])
            sheet.write_formula(summary_row, 14, f'=L{summary_row+1}/N{summary_row+1}', formats['percentage'])
            sheet.write_formula(summary_row, 15, f'=M{summary_row+1}/N{summary_row+1}', formats['percentage'])
            summary_row += 1

        # Apply border 1 to the summary table
        sheet.conditional_format(9, 10, summary_row - 1, 15, {'type': 'no_blanks', 'format': formats['border_1']})

