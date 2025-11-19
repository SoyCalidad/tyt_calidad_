# -*- coding: utf-8 -*-
import base64
import io
from datetime import date, datetime
from math import ceil

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from PIL import Image
from PIL import Image, UnidentifiedImageError
import logging 
import binascii

_logger = logging.getLogger(__name__)


class IndividualReport(models.AbstractModel):
    _name = 'report.tyt_audit.audit_checklist_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Lista de verificación"


    def generate_xlsx_report(self, workbook, data, matrixes):
        try:
            for matrix in matrixes:
                sheet = workbook.add_worksheet(str(matrix.name))

                # Definir algunos formatos de celda
                title_format = workbook.add_format({'text_wrap': True, 'bold': True, 'font_size': 10, 'bg_color': '#215967', 'border': 2, 'valign': 'vcenter', 'align': 'center', 'font_color': 'white'})
                title_blank_format = workbook.add_format({'text_wrap': True, 'bold': True,'bg_color': '#B7DEE8', 'font_size': 10, 'border': 2, 'align': 'center'})
                title_format2 = workbook.add_format({'text_wrap': True, 'bold': True, 'font_size': 10, 'bg_color': '#31859B', 'border': 2, 'valign': 'vcenter', 'align': 'center', 'font_color': 'white'})
                header_format = workbook.add_format({'text_wrap': True, 'bold': True, 'bg_color': '#215967', 'font_color': 'white', 'border': 2, 'align': 'center'})
                row_format = workbook.add_format({'text_wrap': True, 'border': 1, 'align': 'center'})
                logo_box_format = workbook.add_format({'text_wrap': True, 'border': 2, 'align': 'center'})
                alt_row_format = workbook.add_format({'text_wrap': True, 'bg_color': '#B6DDE8', 'border': 1, 'align': 'center'})
                percentage_format = workbook.add_format({'num_format': '0.00%','align': 'center','border': 2, 'bold': True,'bg_color': '#B7DEE8'})
                
                # Configuración del formato general del archivo
                # ANCHO DE COLUMNAS
                sheet.set_column('B:B', 4)  # Columna para numeración
                sheet.set_column('C:F', 20)  # Columnas para datos
                sheet.set_column('G:G', 25)
                sheet.set_column('H:J', 20)  # Columnas para datos

                # ALTO DE FILAS
                    # Fila 1 comienza por "0"

                sheet.set_row(3, 30)

                # Cabecera con los títulos según la imagen proporcionada
                sheet.merge_range('B2:C2', 'PROCEDIMIENTO:', title_format)
                sheet.merge_range('D2:F2', matrix.tyt_procedure_description_id.name or '', title_blank_format)
                sheet.write('G2', 'EVALUACIÓN:', title_format)
                sheet.write('H2', '0', title_blank_format)

                sheet.merge_range('B3:C3', 'RESPONSABLE:', title_format)
                sheet.merge_range('D3:F3', matrix.job_id.name or '', title_blank_format)
                sheet.write('G3', 'NO CONFORMIDADES:', title_format)
                sheet.write('H3', '0', title_blank_format)

                sheet.merge_range('B4:C4', 'AUDITADOS:', title_format)
                #Many2many auditors
                auditors = ', '.join(auditor.name for auditor in matrix.employee_ids) or ''
                sheet.merge_range('D4:F4', auditors or '', title_blank_format)

                sheet.write('G4', 'BUENAS PRÁCTICAS:', title_format)
                sheet.write('H4', '0', title_blank_format)

                sheet.merge_range('B5:C5', 'GRUPO AUDITOR:', title_format)
                sheet.merge_range('D5:F5', matrix.team_id.name or '', title_blank_format)

                # Manejo seguro de audit_date dentro de una String en caso el valor sea NULO (Usuario no completó ese valor)
                if matrix.audit_date:
                    audit_date_str = matrix.audit_date.strftime('%d/%m/%Y')
                else:
                    audit_date_str = ''  # Puedes cambiar esto por '' si prefieres dejarlo vacío

                sheet.merge_range('G5:H5', f'FECHA DE AUDITORIA: ({audit_date_str})', title_format2)

                sheet.merge_range('I5:J5', 'SITIO: ( '+ (matrix.tyt_sites_related_id.x_name or '') +')', title_format2)

                sheet.merge_range(
                    'I2:J4', '', logo_box_format )

                company_id = self.env.user.company_id
                if company_id.logo:
                    try:
                        buf_image = io.BytesIO(base64.b64decode(company_id.logo))
                        im = Image.open(buf_image)
                        width, height = im.size
                        image_width = width
                        image_height = height
                        cell_width = 92.0
                        cell_height = 92.0
                        x_offset = 118.0
                        y_offset = 10.0

                        x_scale = cell_width / image_width
                        y_scale = cell_height / image_height
                        sheet.insert_image('I2', "logo.png", {
                            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': x_offset, 'y_offset': y_offset})
                    except (binascii.Error, UnidentifiedImageError, OSError):
                        pass

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


                # ==================
                # ====== DATA ======
                # ==================


                row = 6  # Esto corresponde a la fila 7 en Excel (0-indexed)
                numero_id = 1  # Contador para la columna B                

                # Itera sobre cada planning en planning_ids
                for planning in matrix.planning_ids:
                    # Determina el formato a aplicar basado en la fila actual
                    if numero_id % 2 != 0:
                        current_format = row_format
                    else:
                        current_format = alt_row_format


                    # Escribe el número en la columna B
                    sheet.write(row, 1, numero_id, current_format)

                    # Escribe "Norma ISO 9001:2015" en Columna C
                    iso9001_standard_complete_names = ', '.join(complete_name.combined_name for complete_name in planning.iso_9001_standards_ids) or ''
                    sheet.write(row, 2, iso9001_standard_complete_names, current_format)

                    # Escribe clause_id.name en la columna D
                    clause_name = planning.clause_id.name if planning.clause_id else ''
                    sheet.write(row, 3, clause_name, current_format)

                    # Escribe new_job_id.name en la columna E
                    job_name = planning.new_job_id.name if planning.new_job_id else ''
                    sheet.write(row, 4, job_name, current_format)

                    # Escribe verification en la columna F
                    sheet.write(row, 5, planning.verification or '', current_format)

                    # Escribe finding en la columna G
                    finding_value = dict(planning._fields['finding'].selection).get(planning.finding, '')
                    sheet.write(row, 6, finding_value, current_format)              

                    # Escribe nombres de archivos adjuntos en la columna H
                    evidence_names = ', '.join(evidence.name for evidence in planning.evidence_attachment_ids) or ''
                    sheet.write(row, 7, evidence_names, current_format)

                    # Escribe comment en la columna I
                    sheet.write(row, 8, planning.comment or '', current_format)

                    # Escribe evaluation en la columna J
                    sheet.write(row, 9, planning.evaluation or '', current_format)

                    # Incrementa la fila y el número
                    row += 1
                    numero_id += 1


                # ==================
                # ====== CUENTA DE HALLAZGOS ======
                # ==================

                # Contar las ocurrencias de cada clave en 'finding'
                non_conformity_count = len(
                    matrix.planning_ids.filtered(lambda p: p.finding == 'non_conformity')
                )
                good_practices_count = len(
                    matrix.planning_ids.filtered(lambda p: p.finding == 'good_practices')
                )

                # Calcular el porcentaje de Buenas Prácticas
                total = non_conformity_count + good_practices_count
                if total > 0:
                    good_practices_percentage = good_practices_count / total
                else:
                    good_practices_percentage = 0  # Evita división por cero

                # Escribir el porcentaje en la celda H2
                sheet.write('H2', good_practices_percentage, percentage_format)

                # Escribir los conteos en las celdas H3 y H4
                sheet.write('H3', non_conformity_count, title_blank_format)
                sheet.write('H4', good_practices_count, title_blank_format)


        except Exception as e:
            _logger.info(f"{e}")
            raise UserError(f"Hubo un error al generar el reporte {e}")
