# -*- coding: utf-8 -*-
import base64
import io
from datetime import date, datetime
from math import ceil

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from PIL import Image


class IndividualReport(models.AbstractModel):
    _name = 'report.tyt_audit.audit_checklist_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, matrixes):
        try:
            for matrix in matrixes:
                sheet = workbook.add_worksheet(str(matrix.name))

                # Definir algunos formatos de celda
                title_format = workbook.add_format({'bold': True, 'font_size': 10, 'bg_color': '#215967', 'border': 1, 'align': 'center', 'font_color': 'white'})
                title_blank_format = workbook.add_format({'bold': True,'bg_color': '#B7DEE8', 'font_size': 10, 'border': 1, 'align': 'center'})
                title_format2 = workbook.add_format({'bold': True, 'font_size': 10, 'bg_color': '#31859B', 'border': 1, 'align': 'center', 'font_color': 'white'})
                header_format = workbook.add_format({'bold': True, 'bg_color': '#215967', 'font_color': 'white', 'border': 1, 'align': 'center'})
                row_format = workbook.add_format({'border': 1, 'align': 'center'})
                alt_row_format = workbook.add_format({'bg_color': '#B6DDE8', 'border': 1, 'align': 'center'})

                # Configuración del formato general del archivo
                sheet.set_column('B:B', 4)  # Columna para numeración
                sheet.set_column('C:F', 20)  # Columnas para datos
                sheet.set_column('G:G', 25)
                sheet.set_column('H:J', 20)  # Columnas para datos

                # Cabecera con los títulos según la imagen proporcionada
                sheet.merge_range('B2:C2', 'PROCEDIMIENTO:', title_format)
                sheet.merge_range('D2:F2', '', title_blank_format)
                sheet.write('G2', 'EVALUACIÓN:', title_format)
                sheet.write('H2', '0', title_blank_format)

                sheet.merge_range('B3:C3', 'RESPONSABLE:', title_format)
                sheet.merge_range('D3:F3', '', title_blank_format)
                sheet.write('G3', 'NO CONFORMIDADES:', title_format)
                sheet.write('H3', '0', title_blank_format)

                sheet.merge_range('B4:C4', 'AUDITADO:', title_format)
                sheet.merge_range('D4:F4', '', title_blank_format)
                sheet.write('G4', 'BUENAS PRÁCTICAS:', title_format)
                sheet.write('H4', '0', title_blank_format)

                sheet.merge_range('B5:C5', 'GRUPO AUDITOR:', title_format)
                sheet.merge_range('D5:F5', '', title_blank_format)
                sheet.merge_range('G5:H5', 'FECHA DE AUDITORIA: ()', title_format2)
                sheet.merge_range('I5:J5', 'SITIO: ()', title_format2)

                sheet.merge_range(
                    'I2:J4', '', row_format )

                company_id = self.env.user.company_id

                buf_image = io.BytesIO(base64.b64decode(company_id.logo))
                im = Image.open(buf_image)
                width, height = im.size
                image_width = width
                image_height = height
                cell_width = 92.0
                cell_height = 92.0
                x_offset = 118.0

                x_scale = cell_width/image_width
                y_scale = cell_height/image_height
                sheet.insert_image('I2', "logo.png", {
                    'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': x_offset})

                # Cabecera de la tabla
                headers = ['N°','Norma ISO 9001:2015', 'CLÁUSULA', 'RESPONSABLE', 'VERIFICACIÓN', 'HALLAZGO', 'EVIDENCIA', 'COMENTARIO', 'EVALUACIÓN']
                col_num = 1  # Las columnas empiezan en C
                for header in headers:
                    sheet.write(5, col_num, header, header_format)
                    col_num += 1

                # Llenado de filas con formato alternado
                for row_num in range(6, 20):  # Ejemplo de 12 filas
                    if row_num % 2 == 0:
                        sheet.write(row_num, 1, '', row_format)  # Aplicar el formato de fila
                        for col_num in range(2, 10):
                            sheet.write(row_num, col_num, '', row_format)
                    else:
                        sheet.write(row_num, 1, '', alt_row_format)  # Aplicar el formato de fila alternada
                        for col_num in range(2, 10):
                            sheet.write(row_num, col_num, '', alt_row_format)



        except Exception as e:
            print(e)
            raise UserError("Hubo un error al generar el reporte")
