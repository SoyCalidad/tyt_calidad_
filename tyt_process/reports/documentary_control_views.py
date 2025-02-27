# -*- coding: utf-8 -*-
import base64
import io
from datetime import date, datetime
from math import ceil

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from PIL import Image

class IndividualReport(models.AbstractModel):
    _name = 'report.tyt_process.record_inventory_report'
    _description = "report.tyt_process.record_inventory_report"
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):

        try:
                # Añade una hoja de trabajo
                sheet = workbook.add_worksheet("Inventario")
                sheet2 = workbook.add_worksheet("Inventario Detallado")

                # Definir estilos
                big_header_format = workbook.add_format({'bold': True, 'align': 'center','valign': 'vcenter','border': 1, 'bg_color': '#31869B', 'color': 'white','font_size': 22})
                header_format = workbook.add_format({'bold': True, 'align': 'center','border': 1, 'bg_color': '#31869B', 'color': 'white'})
                cell_format = workbook.add_format({'align': 'center','valign': 'vcenter','border': 1})
                bold_format = workbook.add_format({'bold': True})

                # Título
                sheet.merge_range('E2:H5', 'INVENTARIO DE REGISTROS INTERNOS', big_header_format)
                
                # Logo (si es necesario)
                #sheet.insert_image('B2', '/path/to/logo.png')  # Aquí puedes añadir la ruta de tu logo si es necesario

                # Escribir encabezados
                sheet.write('B9', 'Documento', header_format)
                sheet.write('C9', 'Abreviatura', header_format)
                sheet.write('E9', 'Área', header_format)
                sheet.write('F9', 'Abreviatura', header_format)
                #sheet.write('G9', 'Código', header_format)


                # Ajustar el ancho de las columnas
                sheet.set_column('B:B', 20)
                sheet.set_column('C:C', 15)
                sheet.set_column('E:E', 30)
                sheet.set_column('F:F', 15)
                sheet.set_column('G:G', 15)

                # Ajustar el ancho de las columnas para que el texto se vea bien
                sheet.set_column('C:C', 15)
                sheet.set_column('D:D', 15)
                sheet.set_column('E:E', 30)
                sheet.set_column('F:F', 15)
                sheet.set_column('G:G', 15)
                sheet.set_column('H:H', 60)
                sheet.set_column('I:I', 25)
                sheet.set_column('J:J', 25)
                sheet.set_column('K:K', 60)
                sheet.set_column('M:M', 60)

                # 7. Obtener todos los registros de tyt_docs y mgmt_categ_type
                tyt_docs_records = self.env['documentary.control.tyt_docs'].search([])
                mgmt_categ_type_records = self.env['mgmt.categ.type'].search([])
        
                # 8. Determinar el número máximo de filas a iterar
                max_rows = max(len(tyt_docs_records), len(mgmt_categ_type_records))

                # 9. Iterar y escribir datos en "Inventario" a partir de B10
                for i in range(max_rows):
                    row = 9 + i  # Fila 10 en Excel (índice 9)

                    # Escribir datos de tyt_docs en columnas B y C
                    if i < len(tyt_docs_records):
                        tyt_doc = tyt_docs_records[i]
                        sheet.write(row, 1, tyt_doc.name or '', cell_format)          # Columna B (índice 1)
                        sheet.write(row, 2, tyt_doc.abbreviation or '', cell_format)  # Columna C (índice 2)
                    else:
                        sheet.write(row, 1, '', cell_format)  # Columna B
                        sheet.write(row, 2, '', cell_format)  # Columna C

                    # Escribir datos de mgmt_categ_type en columnas E y F
                    if i < len(mgmt_categ_type_records):
                        area = mgmt_categ_type_records[i]
                        sheet.write(row, 4, area.name or '', cell_format)   # Columna E (índice 4)
                        sheet.write(row, 5, area.code or '', cell_format)   # Columna F (índice 5)
                        #sheet.write(row, 6, area.code or '', cell_format)   # Columna F (índice 5)
                    else:
                        sheet.write(row, 4, '', cell_format)  # Columna E
                        sheet.write(row, 5, '', cell_format)  # Columna F
                        #sheet.write(row, 6, '', cell_format)  # Columna F
                # ==================
                # ====== SHEET 2 ======
                # ==================

                # Ajustar el ancho de las columnas
                sheet2.set_column('B:B', 20)
                sheet2.set_column('C:C', 15)
                sheet2.set_column('E:E', 30)
                sheet2.set_column('F:F', 15)
                sheet2.set_column('G:G', 15)

                # Ajustar el ancho de las columnas para que el texto se vea bien
                sheet2.set_column('C:C', 15)
                sheet2.set_column('D:D', 15)
                sheet2.set_column('E:E', 15)
                sheet2.set_column('F:F', 15)
                sheet2.set_column('G:G', 60)
                sheet2.set_column('H:H', 25)
                sheet2.set_column('I:I', 25)
                sheet2.set_column('J:J', 60)
                sheet2.set_column('K:K', 15)
                sheet2.set_column('L:L', 80)


                headers_g1 = ['Documento', 'Área', 'Consecutivo']
                headers_g2 = ['Prefijo', 'Nombre', 'Responsable', 'Ubicación', 'Etiquetado Procesos']
                # Insertar los encabezados en la fila 19
                for col_num, header1 in enumerate(headers_g1):
                    sheet2.write(2, col_num + 1, header1, header_format)  # Comienza en la columna B (índice 2)

                for col_num, header2 in enumerate(headers_g2):
                    sheet2.write(2, col_num + 5, header2, header_format)  # Comienza en la columna C (índice 3)

                sheet2.write('L3', 'Valores', header_format)

                # ==================
                # ====== DATA ======
                # ==================
                
                # 7. Obtener todos los registros del modelo
                all_records = self.env['documentary.control'].search([])

                # 8. Iterar sobre todos los registros y escribir los datos en "Detalle de Inventario"
                start_row = 3  # Fila 4 en Excel (índice 3)
                for index, record in enumerate(all_records):
                    row = start_row + index

                    sheet2.write(row, 1, record.tyt_document_id.abbreviation or '', cell_format)  # Columna B (índice 1)
                    sheet2.write(row, 2, record.area_id.code or '', cell_format)  # Columna C (índice 2)
                    sheet2.write(row, 3, record.code_number_str or '', cell_format)

                    sheet2.write(row, 5, record.int_code or '', cell_format)  # Columna F (índice 5)
                    sheet2.write(row, 6, record.name or '', cell_format)  # Columna G (índice 6)
                    sheet2.write(row, 7, record.job_id.name if record.job_id else '', cell_format)  # Columna H (índice 7)
                    sheet2.write(row, 8, record.tyt_sites_id.x_name if record.tyt_sites_id else '', cell_format)  # Columna I (índice 8)

                    int_code = record.int_code or ''
                    name = record.name or ''
                    concatenated_value = f"{int_code}_{name}" if int_code or name else ''
                    sheet2.write(row, 9, concatenated_value, cell_format)  # Columna J (índice 9)
                    sheet2.write(row, 11, concatenated_value, cell_format)  # Columna L (índice 11) 


        except Exception as e:
            print(e)
            raise UserError("Hubo un error al generar el reporte")