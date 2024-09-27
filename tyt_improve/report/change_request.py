# -- coding: utf-8 --
import base64
import io
from collections import defaultdict
from PIL import Image
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class NonconformityInventoryMixin(models.AbstractModel):
    _name = 'report.tyt_improve.report_update_notification'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        # Add the company logo

        try:
            for record in records:
                # Añade una hoja de trabajo
                sheet = workbook.add_worksheet("Notificación de Actualización")

                # ==============================
                # Company Logo
                # ==============================

                company_id = self.env.user.company_id

                buf_image = io.BytesIO(base64.b64decode(company_id.logo))
                im = Image.open(buf_image)
                width, height = im.size
                image_width = width
                image_height = height
                cell_width = 130.0
                cell_height = 130.0
                x_offset = 50.0

                x_scale = cell_width/image_width
                y_scale = cell_height/image_height
                sheet.insert_image('D2', "logo.png", {
                    'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': x_offset})

                # Definir colores personalizados
                celeste_oscuro = '#215967'
                celeste_claro = '#31869B'
                blanco = '#FFFFFF'

                # Definir formatos
                header_format = workbook.add_format({'bold': True, 'font_color': blanco, 'bg_color': celeste_oscuro, 'border': 2, 'align': 'center', 'valign': 'vcenter','font_size': 20})
                subheader_format = workbook.add_format({'bold': True, 'font_color': blanco, 'bg_color': celeste_claro, 'border': 1, 'align': 'center', 'valign': 'vcenter'})
                text_format = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'vcenter'})
                date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'border': 1, 'align': 'left', 'valign': 'vcenter'})
                #border_format = workbook.add_format({'border': 2,'border_color': '#000000'})

                # Ajustar tamaño de columnas
                sheet.set_column('A:A', 8)
                sheet.set_column('B:B', 0.5)
                sheet.set_column('C:C', 0.5)
                sheet.set_column('D:D', 25)
                sheet.set_column('E:E', 25)
                sheet.set_column('F:F', 20)
                sheet.set_column('G:G', 15)
                sheet.set_column('H:H', 25)
                sheet.set_column('I:I', 25)
                sheet.set_column('J:J', 20)
                sheet.set_column('K:K', 0.5)
                sheet.set_column('L:L', 0.5)
                
                # Ajustar el alto de las filas
                    # Fila 1 comienza por "0"
                sheet.set_row(12, 6)
                #sheet.set_row(13, 6)
                sheet.set_row(17, 6)   
                sheet.set_row(18, 6)
                sheet.set_row(19, 6)
                #sheet.set_row(23, 15)
                sheet.set_row(24, 9)
                #sheet.set_row(25, 15)
                sheet.set_row(37, 6)
                sheet.set_row(38, 6)

                
                # Título
                sheet.merge_range('E3:I5', 'COMUNICADO DE CAMBIOS EN PROCESO', header_format)
                
                # Logo (si es necesario cargar un logo de la empresa)
                # sheet.insert_image('A1', 'ruta_logo.png', {'x_scale': 0.5, 'y_scale': 0.5})
                
                # Sección de fechas
                sheet.write('D8', 'Fecha de Solicitud', subheader_format)
                sheet.write('E8', str(record.request_date.strftime('%d/%m/%Y') or ''), date_format)
                
                sheet.write('D9', 'Fecha de Autorización', subheader_format)
                sheet.write('E9', '', text_format)  
                
                sheet.write('D10', 'Fecha de Cambio', subheader_format)
                sheet.write('E10', '', text_format)
                
                sheet.write('D11', 'Fecha de liberación', subheader_format)
                sheet.write('E11', '1/2/2021', date_format)
                
                # ==============================
                # MARCO BORDE PRINCIPAL B13:L39
                # ==============================

                # Esquinas
                sheet.write(12, 1, '', workbook.add_format({'left': 2, 'top': 2}))  # B13
                sheet.write(12, 11, '', workbook.add_format({'right': 2, 'top': 2}))  # L13
                sheet.write(38, 1, '', workbook.add_format({'left': 2, 'bottom': 2}))  # B39
                sheet.write(38, 11, '', workbook.add_format({'right': 2, 'bottom': 2}))  # L39

                # Bordes superior e inferior
                for col in range(2, 11):
                    sheet.write(12, col, '', workbook.add_format({'top': 2}))  # Parte superior del marco
                    sheet.write(38, col, '', workbook.add_format({'bottom': 2}))  # Parte inferior del marco

                # Bordes izquierdo y derecho
                for row in range(13, 38):
                    sheet.write(row, 1, '', workbook.add_format({'left': 2}))  # Parte izquierda del marco
                    sheet.write(row, 11, '', workbook.add_format({'right': 2}))  # Parte derecha del marco


                # Cabecera de solicitante y autorizante
                sheet.merge_range('D15:F15', 'Solicitante', subheader_format)
                sheet.merge_range('H15:J15', 'Autorizante', subheader_format)
                

                # Información del solicitante
                sheet.write('D16', 'Nombre', subheader_format)
                sheet.write('D17', record.employee_id.name or '', text_format)
                
                sheet.write('E16', 'Puesto', subheader_format)
                sheet.write('E17', record.employee_id.job_id.name or '', text_format)
                
                sheet.write('F16', 'Sitio', subheader_format)
                sheet.write('F17', record.employee_id.department_id.display_name or '', text_format)

                # Información de autorizante
                sheet.write('H16', 'Nombre', subheader_format)
                sheet.write('H17', 'Guillermo Celedón', text_format)
                
                sheet.write('I16', 'Puesto', subheader_format)
                sheet.write('I17', 'Gerente de RH', text_format)
                
                sheet.write('J16', 'Sitio', subheader_format)
                sheet.write('J17', 'Central', text_format)

                # ==============================
                # Marco interior para C14:K24
                # ==============================

                # Esquinas
                sheet.write(13, 2, '', workbook.add_format({'left': 2, 'top': 2}))  # C14
                sheet.write(13, 10, '', workbook.add_format({'right': 2, 'top': 2}))  # K14
                sheet.write(23, 2, '', workbook.add_format({'left': 2, 'bottom': 2}))  # C24
                sheet.write(23, 10, '', workbook.add_format({'right': 2, 'bottom': 2}))  # K24

                # Bordes superior e inferior
                for col in range(3, 10):
                    sheet.write(13, col, '', workbook.add_format({'top': 2}))  # Parte superior del marco
                    sheet.write(23, col, '', workbook.add_format({'bottom': 2}))  # Parte inferior del marco

                # Bordes izquierdo y derecho
                for row in range(14, 23):
                    sheet.write(row, 2, '', workbook.add_format({'left': 2}))  # Parte izquierda del marco
                    sheet.write(row, 10, '', workbook.add_format({'right': 2}))  # Parte derecha del marco


                # ==============================
                # Marco interior para C26:K38
                # ==============================

                # Esquinas
                sheet.write(25, 2, '', workbook.add_format({'left': 2, 'top': 2}))  # C26
                sheet.write(25, 10, '', workbook.add_format({'right': 2, 'top': 2}))  # K26
                sheet.write(37, 2, '', workbook.add_format({'left': 2, 'bottom': 2}))  # C38
                sheet.write(37, 10, '', workbook.add_format({'right': 2, 'bottom': 2}))  # K38

                # Bordes superior e inferior
                for col in range(3, 10):
                    sheet.write(25, col, '', workbook.add_format({'top': 2}))  # Parte superior del marco
                    sheet.write(37, col, '', workbook.add_format({'bottom': 2}))  # Parte inferior del marco

                # Bordes izquierdo y derecho
                for row in range(26, 37):
                    sheet.write(row, 2, '', workbook.add_format({'left': 2}))  # Parte izquierda del marco
                    sheet.write(row, 10, '', workbook.add_format({'right': 2}))  # Parte derecha del marco



                # ==============================
                # Contenido del Marco
                # ==============================

                # Sección de Procedimiento
                sheet.write('D21', 'Procedimiento', subheader_format)
                sheet.merge_range('E21:G21', record.procedures_char or '', text_format)
                
                # Cláusula
                sheet.write('D23', 'Cláusula', subheader_format)
                sheet.write('E23', ', '.join(record.clause_id.mapped('name')) or '', text_format) #many2many field
                
                # Sección de Narrativa
                sheet.merge_range('D27:J27', 'Narrativa oficial de la cláusula', subheader_format)
                sheet.merge_range('D28:J31', record.clause_narrative or '', text_format)  # Espacio en blanco para la narrativa
                
                # Cambio a realizar
                sheet.merge_range('D32:J32', 'Cambio a realizar', subheader_format)
                sheet.merge_range('D33:J37', 'De acuerdo al Concentrado Operativo...', text_format)
                
                # Definir formato de celdas y detalles estéticos como bordes, colores
                # Ajustar más detalles de formato si es necesario


        except Exception as e:
            print(e)
            raise UserError("Hubo un error al generar el reporte")