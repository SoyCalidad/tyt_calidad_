from odoo import api, fields, models
from odoo.http import request

from collections import defaultdict
from math import ceil
import base64
import io
from PIL import Image


class SurveyReport(models.AbstractModel):
    _name = 'report.tyt_customer_satisfaction_history.report_tyt_ssh'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Customer Satisfaction History' # before: _description = 'Análisis de encuesta'

    def generate_xlsx_report(self, workbook, data, partners):
        """Generate a xls report with the data
        """

        format21_c_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EFEFEF', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': True})
        format21_gray = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        format21_gray_bold = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True,'font_color': 'white',
			'bg_color': '#31879b','border': 2,
			'text_wrap': True,
			'border_color': '#757070', })
        format21_gray_bold_g = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True,
			'bg_color': '#a5a5a5','border': 2,
			'text_wrap': True,
			'border_color': '#757070', })
        format21_gray_bold_sb = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True,
			'bg_color': '#215967','border': 2,
			'text_wrap': True,
            'font_color': 'white',
			'border_color': '#757070', })
        format21_gray_bold_c = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True,
			'bg_color': '#99d0df','border': 2,
			'text_wrap': True,
            'font_color': 'white',
			'border_color': '#757070', })
        format26_c_bold = workbook.add_format(
            {'font_size': 26, 'font_color': 'white',
			'bg_color': '#31879b','border': 2,
			'border_color': '#757070', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_date_center = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'num_format': 'dd/mm/yyyy'}
        )
        format21_justify = workbook.add_format(
            {'font_size': 10, 'align': 'justify', 'valign': 'vcenter', 'bold': False, 'text_wrap': True}
        )
        number = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'num_format': '#,##0'})
        format_number = workbook.add_format(
        {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'num_format': '#,##0.00'})

        sheet = workbook.add_worksheet(
            'General',)
        sheet.hide_gridlines(option=2)
        company_id = self.env.user.company_id

        buf_image = io.BytesIO(base64.b64decode(company_id.logo))
        im = Image.open(buf_image)
        width, height = im.size
        image_width = width
        image_height = height
        cell_width = 80
        cell_height = 60

        x_scale = cell_width/image_width
        y_scale = cell_height/image_height
        sheet.insert_image('B2:B3', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 25})
        
        sheet.merge_range('B2:C3', '', format21_c_bold)
        sheet.merge_range(
            'D2:L6', 'Historico General', format26_c_bold)
        
        sheet.set_column('A:A', 15)
        sheet.set_column('B:N', 20)
        
        locations = ["ARTEAGA", "MERIDA", "GUADALAJARA", "TAPIA", "PUEBLA", "HERMOSILLO", "QUERETARO", "OBISPADO", "TIJUANA"]
        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        sheet.set_column('P:S', 20)

        tyt_satisfaction_survey_ids = self.env['tyt.satisfaction.survey'].search(
            [
                ('create_date', '>=', data['from_date']),
                ('create_date', '<=', data['to_date']),
                ('line_ids', '!=', False),
            ]
        )
        
        current_row = 12
        
        performance_by_location = {
            'ARTEAGA': [0, 0, 0, 0],
            'MERIDA': [0, 0, 0, 0],
            'GUADALAJARA': [0, 0, 0, 0],
            'TAPIA': [0, 0, 0, 0],
            'PUEBLA': [0, 0, 0, 0],
            'HERMOSILLO': [0, 0, 0, 0],
            'QUERETARO': [0, 0, 0, 0],
            'OBISPADO': [0, 0, 0, 0],
            'TIJUANA': [0, 0, 0, 0],
        }
        
        def create_location_table(sheet, location, months, current_row):
            
            tyt_satisfaction_survey_location_ids = self.env['tyt.satisfaction.survey'].search(
            [
                ('create_date', '>=', data['from_date']),
                ('create_date', '<=', data['to_date']),
                ('line_ids', '!=', False),
                ('location', '=', location),
            ]
        )
            
            sheet.merge_range(current_row, 2, current_row, 6, 'Experiencia del Cliente', format21_gray_bold_sb)
            sheet.merge_range(current_row, 7, current_row, 13, 'Evaluación por sección', format21_gray_bold_sb)
            
            current_row += 1
            
            sheet.write(current_row, 1, location, format21_gray_bold_sb)
            
            sheet.write(current_row, 2, 'Promedio', format21_gray_bold_c)
            sheet.write(current_row, 3, 'Total de clientes que respondieron la encuesta', format21_gray_bold_sb)
            sheet.write(current_row, 4, 'Total de Clientes Promotores', format21_gray_bold_sb)
            sheet.write(current_row, 5, 'Total de Clientes Pasivos', format21_gray_bold_sb)
            sheet.write(current_row, 6, 'Total de Clientes Detractores', format21_gray_bold_sb)
         
            sheet.write(current_row, 7, 'Comunicación', format21_gray_bold_sb)
            sheet.write(current_row, 8, 'Atención', format21_gray_bold_sb)
            sheet.write(current_row, 9, 'Desempeño', format21_gray_bold_sb)
            sheet.write(current_row, 10, 'Eficiencia', format21_gray_bold_sb)
            sheet.write(current_row, 11, 'Seguridad y TI', format21_gray_bold_sb)
            sheet.write(current_row, 12, 'Mantenimiento', format21_gray_bold_sb)
            sheet.write(current_row, 13, 'Mejora continua', format21_gray_bold_sb)
            
            current_row += 1
            
            months_dict = {
                'Enero': '01',
                'Febrero': '02',
                'Marzo': '03',
                'Abril': '04',
                'Mayo': '05',
                'Junio': '06',
                'Julio': '07',
                'Agosto': '08',
                'Septiembre': '09',
                'Octubre': '10',
                'Noviembre': '11',
                'Diciembre': '12'
            }
            
            for month_name, month_number in months_dict.items():

                sheet.write(current_row, 1, month_name, format21_gray_bold_sb)
                    
                # Get the total customers in the month
                month_customers = tyt_satisfaction_survey_location_ids.filtered(
                    lambda x: x.create_date.strftime('%m') == month_number
                )

                total_month_customers = len(month_customers)
                
                # Get the category average of each month based line_ids qualification

                category_totals = {
                    'cat_1': 0,
                    'cat_2': 0,
                    'cat_3': 0,
                    'cat_4': 0,
                    'cat_5': 0,
                    'cat_6': 0,
                    'cat_7': 0,
                }

                # Mapeo de las categorías internas a categorías generales
                category_mapping = {
                    'cat_1': ['cat_1_1', 'cat_1_2', 'cat_1_3'],
                    'cat_2': ['cat_2_1', 'cat_2_2'],
                    'cat_3': ['cat_3_1', 'cat_3_2', 'cat_3_3'],
                    'cat_4': ['cat_4_1', 'cat_4_2'],
                    'cat_5': ['cat_5_1', 'cat_5_2', 'cat_5_3'],
                    'cat_6': ['cat_6_1', 'cat_6_2'],
                    'cat_7': ['cat_7_1', 'cat_7_2'],
                }

                total_promoters_qualification = 0
                total_detractors_qualification = 0
                total_passive_qualification = 0
                
                detractors_count = 0
                passive_count = 0
                promoters_count = 0

                for customer in month_customers:
                    total_current_customer = 0
                    for line in customer.line_ids:
                        for category, subcategories in category_mapping.items():
                            if line.internal_category in subcategories:
                                if line.internal_category in ['cat_3_1', 'cat_3_2', 'cat_3_3']:
                                    if line.internal_category == 'cat_3_1':
                                        performance_by_location[location][0] += line.qualification
                                    if line.internal_category == 'cat_3_2':
                                        performance_by_location[location][1] += line.qualification
                                    if line.internal_category == 'cat_3_3':
                                        performance_by_location[location][2] += line.qualification
                                        performance_by_location[location][3] += 1
                                category_totals[category] += line.qualification
                                if 1 <= line.qualification <= 3:
                                    total_detractors_qualification += line.qualification
                                elif 4 <= line.qualification <= 7:
                                    total_passive_qualification += line.qualification
                                elif 8 <= line.qualification <= 10:
                                    total_promoters_qualification += line.qualification
                                total_current_customer +=line.qualification
                    total_current_customer = total_current_customer / 17
                    if 1 <= total_current_customer <= 3:
                        detractors_count += 1
                    elif 4 <= total_current_customer <= 7:
                        passive_count += 1
                    elif 8 <= total_current_customer <= 10:
                        promoters_count += 1

                # Get category averages
                category_averages = {
                    'cat_1': category_totals['cat_1'] / 3 / total_month_customers if total_month_customers > 0 else 0,
                    'cat_2': category_totals['cat_2'] / 2 / total_month_customers if total_month_customers > 0 else 0,
                    'cat_3': category_totals['cat_3'] / 3 / total_month_customers if total_month_customers > 0 else 0,
                    'cat_4': category_totals['cat_4'] / 2 / total_month_customers if total_month_customers > 0 else 0,
                    'cat_5': category_totals['cat_5'] / 3 / total_month_customers if total_month_customers > 0 else 0,
                    'cat_6': category_totals['cat_6'] / 2 / total_month_customers if total_month_customers > 0 else 0,
                    'cat_7': category_totals['cat_7'] / 2 / total_month_customers if total_month_customers > 0 else 0,
                }
                
                total_average = sum(category_averages.values()) / len(category_averages)
  
                sheet.write(current_row, 2, f"{total_average:.2f}", format21_left)
                sheet.write(current_row, 3, total_month_customers, format21_left)
                sheet.write(current_row, 4, promoters_count, format21_left)
                sheet.write(current_row, 5, passive_count, format21_left)
                sheet.write(current_row, 6, detractors_count, format21_left)
                sheet.write(current_row, 7, f"{category_averages['cat_1']:.2f}", format21_left)
                sheet.write(current_row, 8, f"{category_averages['cat_2']:.2f}", format21_left)
                sheet.write(current_row, 9, f"{category_averages['cat_3']:.2f}", format21_left)
                sheet.write(current_row, 10, f"{category_averages['cat_4']:.2f}", format21_left)
                sheet.write(current_row, 11, f"{category_averages['cat_5']:.2f}", format21_left)
                sheet.write(current_row, 12, f"{category_averages['cat_6']:.2f}", format21_left)
                sheet.write(current_row, 13, f"{category_averages['cat_7']:.2f}", format21_left)
                
                current_row += 1

            return current_row

        for location in locations:
            create_location_table(sheet, location, months, current_row)
            current_row += 14
            
        print ('performance_by_location', performance_by_location)
            
        sheet.merge_range('Q2:S2', 'Desempeño', format21_gray_bold)
        sheet.write('Q3', 'Operaciones', format21_gray_bold_sb)
        sheet.write('R3', 'Calidad', format21_gray_bold_sb)
        sheet.write('S3', 'Reclutamiento', format21_gray_bold_sb)
        row_locations = 4
        for location in locations:
            operation_average = performance_by_location[location][0] / performance_by_location[location][3] if performance_by_location[location][3] > 0 else 0
            quality_average = performance_by_location[location][1] / performance_by_location[location][3] if performance_by_location[location][3] > 0 else 0
            recruitment_average = performance_by_location[location][2] / performance_by_location[location][3] if performance_by_location[location][3] > 0 else 0
            sheet.write(f'P{row_locations}', location, format21_gray_bold_sb)
            sheet.write(f'Q{row_locations}', f"{operation_average:.2f}", format21_left)
            sheet.write(f'R{row_locations}', f"{quality_average:.2f}", format21_left)
            sheet.write(f'S{row_locations}', f"{recruitment_average:.2f}", format21_left)
            row_locations += 1

        sheet2 = workbook.add_worksheet("Histórico")
        
        buf_image = io.BytesIO(base64.b64decode(company_id.logo))
        im = Image.open(buf_image)
        width, height = im.size
        image_width = width
        image_height = height
        cell_width = 80
        cell_height = 60

        x_scale = cell_width/image_width
        y_scale = cell_height/image_height
        sheet2.insert_image('B2:B3', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 25})
        
        sheet2.merge_range('B2:C3', '', format21_c_bold)
        sheet2.merge_range(
            'D2:L6', 'HISTORICO SATISFACCION DEL CLIENTE', format26_c_bold)
        
        sheet2.set_column('A:B', 10)
        sheet2.set_column('C:I', 15)
        sheet2.set_column('J:AH', 25)

        current_row = 8
        
        sheet2.merge_range(current_row, 1, current_row, 8, 'DATOS GENERALES', format21_gray_bold_sb)
        sheet2.merge_range(current_row, 9, current_row, 12, 'COMUNICACIÓN', format21_gray_bold_sb)
        sheet2.merge_range(current_row, 13, current_row, 15, 'ATENCIÓN', format21_gray_bold_sb)
        sheet2.merge_range(current_row, 16, current_row, 19, 'DESEMPEÑO', format21_gray_bold_sb)
        sheet2.merge_range(current_row, 20, current_row, 22, 'EFICIENCIA', format21_gray_bold_sb)
        sheet2.merge_range(current_row, 23, current_row, 26, 'SEGURIDAD', format21_gray_bold_sb)
        sheet2.merge_range(current_row, 27, current_row, 29, 'MANTENIMIENTO', format21_gray_bold_sb)
        sheet2.merge_range(current_row, 30, current_row, 33, 'MEJORA CONTINUA', format21_gray_bold_sb)
        
        current_row += 1
        
        sheet2.write(current_row, 1, 'ID', format21_gray_bold_sb)
        sheet2.write(current_row, 2, 'MES', format21_gray_bold_sb)
        sheet2.write(current_row, 3, 'Sitio', format21_gray_bold_sb)
        sheet2.write(current_row, 4, 'Fecha_registro', format21_gray_bold_sb)
        sheet2.write(current_row, 5, 'Nombre', format21_gray_bold_sb)
        sheet2.write(current_row, 6, 'Puesto', format21_gray_bold_sb)
        sheet2.write(current_row, 7, 'Campaña', format21_gray_bold_sb)
        sheet2.write(current_row, 8, 'Empresa', format21_gray_bold_sb)
        
        for i, line in enumerate(tyt_satisfaction_survey_ids[0].line_ids, 9):
            sheet2.write(current_row, i, line.name, format21_gray_bold_sb)
        
        current_row += 1
        
        spanish_month = {
            '01': 'Enero',
            '02': 'Febrero',
            '03': 'Marzo',
            '04': 'Abril',
            '05': 'Mayo',
            '06': 'Junio',
            '07': 'Julio',
            '08': 'Agosto',
            '09': 'Septiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Diciembre'
        }
        
        for i, survey in enumerate(tyt_satisfaction_survey_ids, 1):
            sheet2.write(current_row, 1, i, format21_left)
            sheet2.write(current_row, 2, spanish_month[survey.create_date.strftime('%m')], format21_left)
            sheet2.write(current_row, 3, '', format21_left)
            sheet2.write(current_row, 4, survey.create_date.strftime('%d/%m/%Y'), format21_left)
            sheet2.write(current_row, 5, survey.partner_name, format21_left)
            sheet2.write(current_row, 6, survey.job, format21_left)
            sheet2.write(current_row, 7, survey.campaign, format21_left)
            sheet2.write(current_row, 8, survey.partner_company, format21_left)
 
            for j, line in enumerate(survey.line_ids, 9):
                
                cat_text_fields = ['cat_1_4', 'cat_2_3', 'cat_3_4', 'cat_4_3', 'cat_5_4', 'cat_6_3', 'cat_7_3', 'cat_7_4']
                
                if line.internal_category in cat_text_fields:
                    value = line.text
                else:
                    value = line.qualification
                
                sheet2.write(current_row, j, value, format21_left)
                
            current_row += 1
