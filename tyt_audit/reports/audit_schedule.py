# -*- coding: utf-8 -*-
import base64
import io
from datetime import date, datetime
from math import ceil

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from PIL import Image
from PIL import Image, UnidentifiedImageError
#from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class IndividualReport(models.AbstractModel):
    _name = 'report.tyt_audit.audit_schedule_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = "report.tyt_audit.audit_schedule_report"


    def generate_xlsx_report(self, workbook, data, matrixes):
        try:
            for matrix in matrixes:
                
                if not matrix.sites_id or not matrix.sites_id.x_name:
                    raise UserError("Debe asignar un 'SITIO' para descargar el reporte de 'Cronograma de Auditoría'.")

                # Definir algunos formatos de celda
                title_format = workbook.add_format({'bold': True, 'font_size': 12, 'bg_color': '#215967', 'border': 2, 'align': 'center', 'valign': 'vcenter', 'font_color': 'white'})
                title_blank_format = workbook.add_format({'bold': True,'bg_color': '#B7DEE8', 'font_size': 10, 'border': 1, 'align': 'center'})
                title_format2 = workbook.add_format({'bold': True, 'font_size': 33, 'bg_color': '#31859B', 'border': 2, 'align': 'center', 'valign': 'vcenter', 'font_color': 'white'})
                s1_title_format2 = workbook.add_format({'text_wrap': True,'bold': True, 'font_size': 24, 'bg_color': '#31859B', 'border': 2, 'align': 'center', 'valign': 'vcenter', 'font_color': 'white'})
                header_format = workbook.add_format({'bold': True, 'bg_color': '#215967', 'font_color': 'white', 'border': 1, 'align': 'center'})
                row_format = workbook.add_format({'text_wrap': True, 'border': 1, 'align': 'center','valign': 'vcenter'})
                s1_row_format = workbook.add_format({'text_wrap': True, 'border': 1,'font_size': 12, 'align': 'center','valign': 'vcenter'})
                alt_row_format = workbook.add_format({'bg_color': '#B6DDE8', 'border': 1, 'align': 'center'})
                header_date_format = workbook.add_format({'num_format': 'dd/mm/yyyy','align': 'center','valign': 'vcenter','border': 2, 'bg_color': '#B7DEE8', 'font_size': 12, 'bold': True})
                header_weekdate_format = workbook.add_format({'align': 'center','valign': 'vcenter','border': 2, 'bg_color': '#B7DEE8', 'font_size': 12, 'bold': True})
                done_row_format = workbook.add_format({'text_wrap': True, 'border': 1, 'align': 'center','valign': 'vcenter'})
                s1_sites_row = workbook.add_format({'text_wrap': True, 'border': 1, 'align': 'center','valign': 'vcenter','font_size': 12, 'bg_color': '#AEABAB'})

                # Descriptions Style
                vertical_description_1 = workbook.add_format({'bg_color': '#66FF66', 'text_wrap': True,'valign': 'vcenter','align': 'center','rotation': 90,'border': 2,'font_size': 14,'bold': True,})
                vertical_description_2 = workbook.add_format({'bg_color': '#FFC000', 'text_wrap': True,'valign': 'vcenter','align': 'center','rotation': 90,'border': 2,'font_size': 14,'bold': True,})
                vertical_description_3 = workbook.add_format({'bg_color': '#FF6600', 'text_wrap': True,'valign': 'vcenter','align': 'center','rotation': 90,'border': 2,'font_size': 14,'bold': True,})
                vertical_description_4 = workbook.add_format({'bg_color': '#6699FF', 'text_wrap': True,'valign': 'vcenter','align': 'center','rotation': 90,'border': 2,'font_size': 14,'bold': True,})
                vertical_description_5 = workbook.add_format({'bg_color': '#BF9000', 'text_wrap': True,'valign': 'vcenter','align': 'center','rotation': 90,'border': 2,'font_size': 14,'bold': True,})
                vertical_description_6 = workbook.add_format({'bg_color': '#FF99CC', 'text_wrap': True,'valign': 'vcenter','align': 'center','rotation': 90,'border': 2,'font_size': 14,'bold': True,})

                auditor_check_and_done_format = workbook.add_format({'bg_color': '#66FF66', 'text_wrap': True, 'border': 1, 'align': 'center','valign': 'vcenter'})
                auditor_check_or_done_format = workbook.add_format({'bg_color': '#FFBD33', 'text_wrap': True, 'border': 1, 'align': 'center','valign': 'vcenter'})
                fixed_date_check_format = workbook.add_format({'bg_color': '#EB1919', 'text_wrap': True, 'border': 1, 'align': 'center','valign': 'vcenter'})

                sheet1 = workbook.add_worksheet(str("Asignación por Auditor"))

                # Configuración del formato general del archivo

                # ANCHO DE COLUMNAS
                sheet1.set_column('A:A', 4)  # Columna marco
                sheet1.set_column('B:B', 10) # Columna marco
                sheet1.set_column('C:C', 25)  # Columna Sitios
                sheet1.set_column('D:D', 40)  # Columna Auditores Responsables
                sheet1.set_column('E:K', 40)

                # ALTO DE FILAS
                    # Fila 1 comienza por "0"

                sheet1.set_row(11, 25) # MARGIN

                sheet1.set_row(12, 35)
                sheet1.set_row(14, 18)

                # HEADER LOGO
                company_id = self.env.user.company_id
                if company_id.logo:
                    try:
                        buf_image = io.BytesIO(base64.b64decode(company_id.logo))
                        im = Image.open(buf_image)
                        width, height = im.size
                        image_width = width
                        image_height = height
                        cell_width = 184.0
                        cell_height = 184.0
                        x_offset = 0.0

                        x_scale = cell_width/image_width
                        y_scale = cell_height/image_height
                        sheet1.insert_image('C5', "logo.png", {
                            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': x_offset})
                    except (base64.binascii.Error, UnidentifiedImageError, OSError):
                        pass

                # HEADER
                sheet1.merge_range('C12:D14', 'CRONOGRAMA DE AUDITORIAS MENSUALES POR AUDITOR', s1_title_format2)
                


                sheet1.write('C15', 'Sitio', title_format)
                sheet1.write('D15', 'Auditores Responsables', title_format)

                sheet1.merge_range('E12:K12', 'MES', title_format)

                sheet1.write('E13', 'RECURSOS HUMANOS', header_weekdate_format)
                sheet1.write('F13', 'CALIDAD', header_weekdate_format)
                sheet1.write('G13', 'SISTEMAS', header_weekdate_format)
                sheet1.write('H13', 'REGLAMENTO INTERNO', header_weekdate_format)
                sheet1.write('I13', 'OPERACIONES', header_weekdate_format)
                sheet1.write('J13', 'ADICIONALES', header_weekdate_format)

                sheet1.merge_range('E14:E15', 'SEM', title_format)
                sheet1.merge_range('F14:F15', 'SEM', title_format)
                sheet1.merge_range('G14:G15', 'SEM', title_format)
                sheet1.merge_range('H14:H15', 'SEM', title_format)
                sheet1.merge_range('I14:I15', 'SEM', title_format)
                sheet1.merge_range('J14:J15', 'SEM', title_format)

                sheet1.merge_range('K13:K15', 'TOTALES', header_weekdate_format)


                # DATA
                '''
                sheet1.write('C16', 'GUADALAJARA', s1_sites_row)
                sheet1.write('C17', 'HERMOSILLO', s1_sites_row)
                sheet1.write('C18', 'PUEBLA CAT', s1_sites_row)
                sheet1.write('C19', 'PUEBLA', s1_sites_row)
                sheet1.write('C20', 'QUERETARO', s1_sites_row)
                sheet1.write('C21', 'TAPIA', s1_sites_row)
                sheet1.write('C22', 'ARTEAGA', s1_sites_row)
                sheet1.write('C23', 'MERIDA', s1_sites_row)
                '''

                # Iniciar en la fila 16 (índice 15)
                start_row = 15                
                # Asegurarse de que audit_plan_tyt_auditor_id esté presente
                if not matrix.audit_plan_tyt_auditor_id:
                    continue

                # Iterar sobre cada schedule en schedule_ids
                for schedule in matrix.audit_plan_tyt_auditor_id.schedule_ids:
                    # Columnas (0-based):
                    # C -> 2, D -> 3, E -> 4, F -> 5, G -> 6, H -> 7, I -> 8, J -> 9, K -> 10
                    col_C = 2
                    col_D = 3
                    col_E = 4
                    col_F = 5
                    col_G = 6
                    col_H = 7
                    col_I = 8
                    col_J = 9
                    col_K = 10

                    # Escribir Nombre del Sitio en Columna C
                    site_name = schedule.tyt_sites_id.x_name or ''
                    sheet1.write(start_row, col_C, site_name, s1_sites_row)

                    # Escribir Auditores Responsables en Columna D
                    auditors = ', '.join(auditor.name for auditor in schedule.responsible_auditors_id) or ''
                    sheet1.write(start_row, col_D, auditors, s1_row_format)

                    # Escribir Recursos Humanos en Columna E
                    sheet1.write(start_row, col_E, schedule.human_resources or 0, s1_row_format)

                    # Escribir Calidad en Columna F
                    sheet1.write(start_row, col_F, schedule.quality or 0, s1_row_format)

                    # Escribir Sistemas en Columna G
                    sheet1.write(start_row, col_G, schedule.systems or 0, s1_row_format)

                    # Escribir Reglamento Interno en Columna H
                    sheet1.write(start_row, col_H, schedule.internal_regulations or 0, s1_row_format)

                    # Escribir Operaciones en Columna I
                    sheet1.write(start_row, col_I, schedule.operations or 0, s1_row_format)

                    # Escribir Adicionales en Columna J
                    sheet1.write(start_row, col_J, schedule.additionals or 0, s1_row_format)

                    # Escribir Total en Columna K
                    sheet1.write(start_row, col_K, schedule.total_sum or 0, s1_row_format)

                    # Mover a la siguiente fila
                    start_row += 1

                # =====================================================
                # === SHEET 2 ===
                # =====================================================


                sheet2 = workbook.add_worksheet(str(matrix.sites_id.x_name))


                # Configuración del formato general del archivo

                # ANCHO DE COLUMNAS
                sheet2.set_column('A:A', 4)  # Columna marco
                sheet2.set_column('C:C', 75)  # Columnas Actividades
                sheet2.set_column('D:D', 40)
                sheet2.set_column('E:E', 20)
                sheet2.set_column('F:F', 45)  # Columnas para datos

                sheet2.set_column('G:XFD', 16) # ==== COLUMNA DE FECHAS ====


                # ALTO DE FILAS
                    # Fila 1 comienza por "0"

                sheet2.set_row(10, 30) # FECHAS
                
                for row in range(12, 44):
                    sheet2.set_row(row, 30)

                sheet2.set_row(33, 45)
                sheet2.set_row(35, 45)
                sheet2.set_row(36, 45)
                sheet2.set_row(38, 60)

                # CUADRO HEADER
                sheet2.write('C1', 'TOTAL AUDITORIAS', title_format)
                sheet2.write('D1', 'PROMEDIO', title_format)

                sheet2.write('C2', '1', title_format)
                sheet2.write('D2', '95%', title_format)
                sheet2.write('C3', '2', title_format)
                sheet2.write('D3', '90 - 94%', title_format)
                sheet2.write('C4', '3', title_format)
                sheet2.write('D4', '89%', title_format)


                # Cabecera con los títulos según la imagen proporcionada

                sheet2.merge_range('C10:F12', 'CRONOGRAMA DE AUDITORÍAS', title_format2)
                sheet2.write('C13', 'Actividad', title_format)
                sheet2.write('D13', 'Auditores Responsables', title_format)
                sheet2.write('E13', 'Semanas * Auditar', title_format)
                sheet2.write('F13', 'AUDITORIAS A COMPARTIR POR PROCESO', title_format)

                # Fila inicial para las descripciones y actividades
                fila_inicial = 13  # Fila 13
                columna_actividad = 2  # Columna C

                # Obtener las descripciones y actividades dinámicamente
                descriptions = self.env['audit.plan.schedule.descriptions'].search([])

                # Colores cíclicos para descripciones
                color_formats = [
                    vertical_description_1,
                    vertical_description_2,
                    vertical_description_3,
                    vertical_description_4,
                    vertical_description_5,
                    vertical_description_6,
                ]

                # Recorrer las descripciones y asociarlas con actividades
                for idx, description in enumerate(descriptions):
                    # Obtener actividades asociadas a la descripción
                    activities = self.env['audit.plan.schedule.activities'].search([
                        ('description_id', '=', description.id)
                    ])
                    
                    if not activities:
                        continue  # Si no hay actividades, pasa a la siguiente descripción

                    # Asignar color cíclico para la descripción
                    color_format = color_formats[idx % len(color_formats)]

                    # Determinar la fila final para esta descripción
                    fila_final = fila_inicial + len(activities) - 1

                    # Escribir la descripción en la columna B (ajustada a las actividades)
                    sheet2.merge_range(f'B{fila_inicial + 1}:B{fila_final + 1}', description.name, color_format)

                    # Función para calcular altura adaptable
                    def calculate_row_height(text, column_width, base_height=22.5):
                        # Estimar cuántas líneas se necesitarán
                        lines = ceil(len(text) / (column_width * 1.2))  # Ajuste empírico (1.2 para márgenes y espacios)
                        return base_height * lines  # Multiplicar por el número de líneas

                    # Escribir actividades en la columna C y ajustar el alto de fila
                    for index, activity in enumerate(activities):
                        fila = fila_inicial + index
                        sheet2.write(fila, columna_actividad, activity.name, row_format)
                        
                        # Calcular la altura de la fila según el contenido
                        text_length = len(activity.name or "")  # Longitud del texto
                        column_width = 56  # Ancho de la columna configurado
                        row_height = calculate_row_height(activity.name, column_width)
                        
                        # Ajustar la altura de la fila
                        sheet2.set_row(fila, row_height)

                    # Avanzar la fila inicial para la próxima descripción
                    fila_inicial = fila_final + 1  # Continúa desde la siguiente fila


                # "DESCRIPCIONES" columna B
                # sheet2.merge_range('B14:B17', 'CALIDAD', vertical_description_1)
                # sheet2.merge_range('B18:B21', 'SISTEMAS', vertical_description_2)
                # sheet2.merge_range('B22:B25', 'OP', vertical_description_3)
                # sheet2.merge_range('B26:B31', 'RECURSOS HUMANOS', vertical_description_4)
                # sheet2.merge_range('B32:B40', 'REGLAMENTO INTERNO', vertical_description_5)
                # sheet2.merge_range('B41:B44', 'ADICIONALES', vertical_description_6)


            # ======= IMPRIMIR HEADER :FECHAS PROGRAMADAS (audit.plan.schedule.line)=======

            if matrix.schedule_ids:
                first_schedule = matrix.schedule_ids[0]  # Obtener el primer registro de schedule_ids
                line_ids = first_schedule.line_ids  # Obtener los line_ids relacionados

                # Fila 11 en Excel corresponde al índice 10 (0-indexado)
                date_header_row = 10
                columna_inicial = 6  # Columna "G" corresponde al índice 6

                # Definir una lista de días de la semana en español
                weekdays = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']                

                for idx, line in enumerate(line_ids):
                    if line.scheduled_date:
                        # =====================================================
                        # === Escribir la fecha en la celda correspondiente ===
                        # =====================================================
                        sheet2.write(date_header_row, columna_inicial + idx, line.scheduled_date, header_date_format)
                        

                        # Convertir la fecha de Odoo a un objeto datetime.date
                        scheduled_date = fields.Date.from_string(line.scheduled_date)
                        
                        # Obtener el número del día de la semana (0=Monday, 6=Sunday)
                        weekday_number = scheduled_date.weekday()
                        
                        # Obtener el nombre del día en español ('Lunes', 'Martes', 'Miércoles' ...)
                        weekday_name = weekdays[weekday_number]
                        
                        sheet2.write(date_header_row + 2, columna_inicial + idx, weekday_name, header_weekdate_format)


                        # MARGIN
                        sheet2.write(date_header_row - 1, columna_inicial + idx, "", title_format)
                        sheet2.write(date_header_row + 1, columna_inicial + idx, "", title_format)


            # ======= IMPRIMIR valores de  CAMPOS "DONE" (G) , AUDITORES (D), SEMANAS TOTALES (E) =======

            if matrix.schedule_ids:
                starting_row = 13  # Excel fila 14 (0-indexado)

                # Filtrar schedule_ids según schedule.sites_id == matrix.sites_id
                filtered_schedule_ids = matrix.schedule_ids.filtered(lambda s: s.sites_id == matrix.sites_id)

                for schedule in filtered_schedule_ids:
                    line_ids = schedule.line_ids

                    done_column = 6  # Columna "G" (0-indexado)
                    auditors_column = 3
                    totalweeks_column = 4
                    blank_column = 5
                    
                    auditors_value = ', '.join(schedule.responsible_auditors_id.mapped('name'))
                    totalweeks_value = schedule.total_weeks


                    sheet2.write(starting_row, auditors_column, auditors_value, row_format)
                    sheet2.write(starting_row, totalweeks_column, totalweeks_value, row_format)
                    sheet2.write(starting_row, blank_column, "", row_format)

                    for line in line_ids:
                        value = "X" if line.done else ""

                        if line.fixed_date_check:
                            done_row_line_format = fixed_date_check_format
                        elif line.auditor_check and line.done:
                            done_row_line_format = auditor_check_and_done_format
                        elif line.auditor_check or line.done:
                            done_row_line_format = auditor_check_or_done_format
                        else:
                            done_row_line_format = done_row_format

                        sheet2.write(starting_row, done_column, value, done_row_line_format)
                        done_column += 1  # Mover a la siguiente columna (H, I, J, ...)
                    
                    starting_row += 1  # Mover a la siguiente fila (15, 16, 17, ...)


        except Exception as e:
            print(e)
            raise UserError("Hubo un error al generar el reporte")
