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
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):

        try:
            for record in records:
                # Añade una hoja de trabajo
                sheet = workbook.add_worksheet("Inventario")

                # Definir estilos
                big_header_format = workbook.add_format({'bold': True, 'align': 'center','valign': 'vcenter','border': 1, 'bg_color': '#31869B', 'color': 'white','font_size': 22})
                header_format = workbook.add_format({'bold': True, 'align': 'center','border': 1, 'bg_color': '#31869B', 'color': 'white'})
                cell_format = workbook.add_format({'align': 'center','valign': 'vcenter','border': 1})
                bold_format = workbook.add_format({'bold': True})

                # Título
                sheet.merge_range('E2:H5', 'INVENTARIO DE REGISTROS INTERNOS', big_header_format)
                
                # Logo (si es necesario)
                #sheet.insert_image('B2', '/path/to/logo.png')  # Aquí puedes añadir la ruta de tu logo si es necesario

                # Definir los datos estáticos de la tabla Documentos y Áreas
                documentos = [
                    ('Documento', 'Abreviatura'),
                    ('Procedimiento', 'P'),
                    ('Política', 'O'),
                    ('Apéndice', 'A'),
                    ('Manual', 'M'),
                ]

                areas = [
                    ('Área', 'Abreviatura', 'Código'),
                    ('Dirección', 'D', 'PO-01'),
                    ('Operación', 'O', 'PO-01'),
                    ('Recursos Humanos', 'RH', 'PRH-01'),
                    ('Reclutamiento y Selección', 'RS', 'PRS-01'),
                    ('Calidad', 'CC', 'PCC-01'),
                    ('Comercial', 'C', 'PC-01'),
                    ('Finanzas', 'F', 'PF-01'),
                    ('Tecnología de Información', 'TI', 'PTI-01'),
                ]

                # Escribir encabezados
                sheet.write('B9', 'Documento', header_format)
                sheet.write('C9', 'Abreviatura', header_format)
                sheet.write('E9', 'Área', header_format)
                sheet.write('F9', 'Abreviatura', header_format)
                sheet.write('G9', 'Código', header_format)

                # Insertar los datos de Documentos
                row = 9
                for doc in documentos[1:]:
                    sheet.write(row, 1, doc[0], cell_format)
                    sheet.write(row, 2, doc[1], cell_format)
                    row += 1
                
                # Insertar los datos de Áreas
                row = 9
                for area in areas[1:]:
                    sheet.write(row, 4, area[0], cell_format)
                    sheet.write(row, 5, area[1], cell_format)
                    sheet.write(row, 6, area[2], cell_format)
                    row += 1

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

                headers_g1 = ['Documento', 'Área', 'Consecutivo']
                headers_g2 = ['Prefijo', 'Nombre', 'Responsable', 'Ubicación', 'Etiquetado Procesos']
                # Insertar los encabezados en la fila 19
                for col_num, header1 in enumerate(headers_g1):
                    sheet.write(19, col_num + 2, header1, header_format)  # Comienza en la columna C (índice 2)

                for col_num, header2 in enumerate(headers_g2):
                    sheet.write(19, col_num + 6, header2, header_format)  # Comienza en la columna G (índice 3)

                sheet.write('M20', 'Valores', header_format)




        except Exception as e:
            print(e)
            raise UserError("Hubo un error al generar el reporte")