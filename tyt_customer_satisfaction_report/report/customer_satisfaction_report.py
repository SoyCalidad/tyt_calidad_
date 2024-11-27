from odoo import api, fields, models
from odoo.http import request

from collections import defaultdict
from math import ceil
import base64
import io
from PIL import Image


class SurveyReport(models.AbstractModel):
    _name = 'report.customer_satisfaction_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Customer Satisfaction Report' # before: _description = 'Análisis de encuesta'

    def generate_xlsx_report(self, workbook, data, partners):
        """Generate a xls report with the data
        """

        format21_c_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EFEFEF', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
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
            'NPS por Sitio',)
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
            'D2:L3', 'Encuesta de Satisfacción CX', format26_c_bold)
        
        sheet.merge_range('C5:G5', 'Experiencia del Cliente', format21_gray_bold)
        sheet.write('B6', 'Sitio', format21_gray_bold_sb)
        sheet.write('C6', 'Promedio', format21_gray_bold_sb)
        sheet.write('D6', 'Total de clientes que respondieron la encuesta', format21_gray_bold_sb)
        sheet.write('E6', 'Total de Clientes Promotores', format21_gray_bold_sb)
        sheet.write('F6', 'Total de Clientes Pasivos', format21_gray_bold_sb)
        sheet.write('G6', 'Total de Clientes Detractores', format21_gray_bold_sb)
        
        sheet.set_column('A:A', 15) 
        sheet.set_column('B:N', 20)
        
        
        sheet.merge_range('H5:N5', 'Experiencia del Cliente', format21_gray_bold)
        sheet.set_row(6, 20) 
        col = 7
        
        for question in partners.question_and_page_ids:
            if question.is_page:
                title = question.title
                sheet.write(5, col, title, format21_gray_bold_sb)
                col += 1
        
        row = 8
        sheet.merge_range('C{}:E{}'.format(row,row),'Desempeño' , format21_gray_bold)
        sheet.write(row, 2, 'Operaciones', format21_gray_bold_sb)
        sheet.write(row, 3, 'Calidad', format21_gray_bold_sb)
        sheet.write(row, 4, 'Reclutamiento', format21_gray_bold_sb)
        row += 1
        
        
        sheet = workbook.add_worksheet(
            'Satisfaccion_clientes - General',)
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
            'D2:L3', 'INFORME SATISFACCIÓN', format26_c_bold)
        
        sheet.set_column('A:A', 15) 
        sheet.set_column('B:H', 20)
        
        sheet.merge_range('B7:H7', 'DATOS GENERALES	', format21_gray_bold)
        sheet.write('B8', 'ID', format21_gray_bold_sb)
        sheet.write('C8', 'Sitio', format21_gray_bold_sb)
        sheet.write('D8', 'Fecha de Registro', format21_gray_bold_sb)
        sheet.write('E8', 'Nombre', format21_gray_bold_sb)
        sheet.write('F8', 'Puesto', format21_gray_bold_sb)
        sheet.write('G8', 'Campaña', format21_gray_bold_sb)
        sheet.write('H8', 'Empresa', format21_gray_bold_sb)
    
    
		
        max_len = 0

        i = 8
        column_ranges_s = []
        column_ranges_e = []
        for question in partners.question_ids:
            if question.question_type == 'matrix':
                column_ranges_s.append(i)
                for label in question.matrix_row_ids:  
                    title = label.value
                    sheet.write(7, i, title, format21_gray_bold)
                    
                    max_len = max(max_len, len(title))
                    sheet.set_column(i, i, 40)
                    i += 1
            else:
                title = question.title
                sheet.write(7, i, title, format21_gray_bold_g)
                max_len = max(max_len, len(title))
                sheet.set_column(i, i, 40)
                
                column_ranges_e.append(i)
                i += 1
        
            
            
        page_titles = []
        j=0
        for question in partners.question_and_page_ids:
            if question.is_page:
                title = question.title
                page_titles.append(title)
                sheet.merge_range(6, column_ranges_s[j], 6, column_ranges_e[j], title, format21_gray_bold_c)
                j += 1
        
        height = ceil(max_len/40)*12
        sheet.set_row(8, height)
        
        sheet.write('D10', 'Promedio', format21_gray_bold_sb)
        row = 10
        
        for question in partners.question_and_page_ids:
            if question.is_page:
                title = question.title
                sheet.write(row, 2, title, format21_gray_bold_sb)
                row += 1