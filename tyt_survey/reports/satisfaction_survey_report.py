from odoo import models
from odoo.exceptions import UserError

class SatisfactionSurveyXlsxReport(models.AbstractModel):
    _name = 'report.tyt_survey.satisfaction_survey_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, surveys):
        try:
            # Determinar el número máximo de preguntas
            max_questions = max(len(survey.line_ids) for survey in surveys)
            
            # Crear hoja
            sheet = workbook.add_worksheet("Satisfaction Surveys")

            # Definir formatos
            title_format = workbook.add_format({
                'bold': True, 'font_size': 16, 'bg_color': '#215967', 'border': 2,
                'align': 'center', 'valign': 'vcenter', 'font_color': 'white'
            })
            header_format = workbook.add_format({
                'bold': True, 'bg_color': '#31859B', 'font_color': 'white', 
                'align': 'center', 'border': 1, 'valign': 'vcenter'
            })
            row_format = workbook.add_format({
                'text_wrap': True, 'align': 'center', 'border': 1, 'valign': 'vcenter'
            })
            fill_format = workbook.add_format({
                'bg_color': '#ffffff', 'border': 1, 'align': 'center', 'valign': 'vcenter'
            })  # Fondo para celdas vacías

            # Generar cabeceras
            headers = [
                'N°', 'NOMBRE', 'PUESTO', 'CORREO', 'EMPRESA', 
                'CAMPAÑA', 'SITIO', 'CREADO EN'
            ]
            for i in range(1, max_questions + 1):
                headers.append(f'PREGUNTA {i}')
                headers.append(f'CALIFICACIÓN {i}')

            # Ajustar ancho de columnas
            column_widths = [5, 20, 20, 25, 20, 20, 15, 15]  # Anchos iniciales
            column_widths.extend([40, 20] * max_questions)  # Anchos para preguntas y calificaciones

            for col_num, width in enumerate(column_widths):
                sheet.set_column(col_num, col_num, width)

            # Ajustar el título dinámicamente
            last_col = len(headers) - 1  # Última columna generada
            last_col_letter = chr(65 + last_col)  # Convertir índice a letra de columna (A, B, C...)
            sheet.merge_range(f'A2:{last_col_letter}2', 'TYT', title_format)

            # Escribir cabeceras
            for col_num, header in enumerate(headers):
                sheet.write(2, col_num, header, header_format)

            # Escribir datos de las encuestas
            for row_num, survey in enumerate(surveys, start=3):
                sheet.write(row_num, 0, row_num - 2, row_format)  # N°
                sheet.write(row_num, 1, survey.partner_name or '', row_format)
                sheet.write(row_num, 2, survey.job or '', row_format)
                sheet.write(row_num, 3, survey.email or '', row_format)
                sheet.write(row_num, 4, survey.partner_company or '', row_format)
                sheet.write(row_num, 5, survey.campaign or '', row_format)
                sheet.write(row_num, 6, survey.location or '', row_format)
                sheet.write(row_num, 7, survey.create_date.strftime('%Y-%m-%d') if survey.create_date else '', row_format)

                # Escribir preguntas y calificaciones
                col_offset = 8  # Comenzar después de las columnas básicas
                for line in survey.line_ids:
                    sheet.write(row_num, col_offset, line.name or '', row_format)  # Pregunta
                    sheet.write(row_num, col_offset + 1, line.qualification or 0, row_format)  # Calificación
                    col_offset += 2

                # Rellenar celdas vacías con fondo si no hay más preguntas
                while col_offset < len(headers):
                    sheet.write(row_num, col_offset, '', fill_format)
                    col_offset += 1

        except Exception as e:
            raise UserError(f"Error generating report: {e}")
