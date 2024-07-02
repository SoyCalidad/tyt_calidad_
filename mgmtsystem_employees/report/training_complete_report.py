# -*- coding: utf-8 -*-
import base64
import io

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from PIL import Image


class ReportTrainingComplete(models.AbstractModel):
    _name = 'report.mgmtsystem_employees.training_complete'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, trainings):
        try:

            format21_c_bold = workbook.add_format({'font_size': 10, 'bg_color':'#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
            format26_c_bold = workbook.add_format({'font_size': 14, 'bg_color':'#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
            format21_left = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
            format21_gray = workbook.add_format({'font_size': 10, 'bg_color':'#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
            format21_gray_bold = workbook.add_format({'font_size': 10, 'bg_color':'#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True,})
            format21_gray_rotate_bold = workbook.add_format({'font_size': 10, 'bg_color':'#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True,})

            format21_c_bold.set_border()
            format26_c_bold.set_border()
            format21_left.set_border()
            format21_gray.set_border()
            format21_gray_bold.set_border()
            format21_gray_rotate_bold.set_border()
            format21_gray_rotate_bold.set_rotation(90)

            sheet = workbook.add_worksheet('Capacitaciones')

            sheet.set_column(0,0,5)
            sheet.set_column(1,1,30)
            sheet.set_column(2,2,11)
            sheet.set_column(3,9,5)
            sheet.set_column(10,10,30)

            sheet.merge_range('A1:B3', '', format21_c_bold)
            sheet.merge_range('C1:J3','BASE DE DATOS DE CAPACITACIONES',format26_c_bold)
            datetime = fields.Datetime.now(self)
            
            sheet.merge_range('K2:K3','Fecha: '+str(datetime),format21_c_bold)

            sheet.merge_range('A4:A7','Nro',format21_gray_bold)
            sheet.merge_range('B4:B7','Tema',format21_gray_bold)
            sheet.merge_range('C4:C7','Fecha',format21_gray_bold)
            sheet.merge_range('D4:D7','Convocados',format21_gray_rotate_bold)
            sheet.merge_range('E4:E7','Asistentes',format21_gray_rotate_bold)

            sheet.merge_range('F4:H4','ASISTENCIA',format21_c_bold)
            sheet.merge_range('F5:F7','Puntuales',format21_gray_rotate_bold)
            sheet.merge_range('G5:G7','Tardanzas',format21_gray_rotate_bold)
            sheet.merge_range('H5:H7','Faltas',format21_gray_rotate_bold)

            sheet.merge_range('I4:J4','EVALUACIÓN',format21_c_bold)
            sheet.merge_range('I5:I7','Aprobados',format21_gray_rotate_bold)
            sheet.merge_range('J5:J7','Desaprobados',format21_gray_rotate_bold)

            sheet.merge_range('K4:K7','Ponente',format21_gray_bold)

            company_id = self.env.user.company_id

            buf_image = io.BytesIO(base64.b64decode(company_id.logo))
            im = Image.open(buf_image)
            width, height = im.size
            image_width = width
            image_height = height
            cell_width = 48.0
            cell_height = 48.0

            x_scale = cell_width/image_width
            y_scale = cell_height/image_height
            sheet.insert_image('A1', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 100})

            row = 7
            count = 0
            for record in trainings:
                column = a_assist = t_assist = f_assist = test_a = test_d = 0
                count += 1
                code = record.code if record.code else ''
                sheet.write('K1','Código: '+ code,format21_c_bold)
                sheet.write(row, column, count, format21_left)
                column += 1
                sheet.write(row, column, record.name, format21_left)
                column += 1
                sheet.write(row, column, str(record.date_training), format21_left)
                column += 1
                sheet.write(row, column, len(record.line_ids), format21_left)
                column += 1
                for each in record.line_ids:
                    if each.assistance == 'A':
                        a_assist += 1
                    elif each.assistance == 'T':
                        t_assist += 1
                    elif each.assistance == 'F':
                        f_assist += 1
                    if each.state_test == 'approved':
                        test_a += 1
                    elif each.state_test == 'disapproved':
                        test_d += 1
                sheet.write(row, column, a_assist+t_assist, format21_left)
                column += 1
                sheet.write(row, column, a_assist, format21_left)
                column += 1
                sheet.write(row, column, t_assist, format21_left)
                column += 1
                sheet.write(row, column, f_assist, format21_left)
                column += 1
                sheet.write(row, column, test_a, format21_left)
                column += 1
                sheet.write(row, column, test_d, format21_left)
                column += 1
                exponent = record.exponent_id.name if record.exponent_id else ''
                sheet.write(row, column, exponent, format21_left)
                column += 1
                row += 1

        except Exception as e:
            print(e)
            raise UserError("Hubo un error al generar el reporte")