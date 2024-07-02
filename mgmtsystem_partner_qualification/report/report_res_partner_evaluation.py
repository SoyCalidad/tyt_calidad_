import base64
import io
from collections import defaultdict

from odoo import api, fields, models
from odoo.http import request
from PIL import Image
from datetime import date


class PartnerEvaluationReport(models.AbstractModel):
    _name = 'report.mgmtsystem_partner_qualification.partner_evaluation'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, evaluations):
        format21_c_bold = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'bg_color': '#A0A0A0', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_left_bold = workbook.add_format(
            {'font_size': 10, 'align': 'left', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'left', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
        format21_center = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
        format_1 = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 1, 'bg_color': '#EEEEEE'})
        format_title = workbook.add_format(
            {'font_size': 13, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'align': 'center', 'bg_color': '#EEEEEE', 'border': 1})

        if data and data.get('is_wizard'):
            evaluations = self.env['res.partner.evaluation.history'].browse(
                data['ids'])
        i = 0
        for evaluation in evaluations:
            partner = evaluation.partner_id
            i += 1
            evaluation_date = evaluation.date_history.strftime(
                '%d-%m-%Y') if evaluation.date_history else ''
            sheet_name = 'Evaluación_' + str(i)
            sheet = workbook.add_worksheet(sheet_name)

            sheet.set_column(0, 0, 9)
            sheet.set_column(1, 1, 15)
            sheet.set_column(2, 2, 9)
            sheet.set_column(3, 3, 56)
            sheet.set_column(4, 6, 10)

            row = 6
            r_col = 0
            col = r_col

            # sheet.merge_range(row, col, row, col+4, "Socio: "+partner.name, format21_left_bold)
            # row += 1
            # sheet.merge_range(row, col, row, col+4, ("Ruc: %s")%(partner.vat or "No establecido"), format21_left_bold)
            # row += 1
            # sheet.merge_range(row, col, row, col+4, "Fecha de evaluación: "+evaluation.date_history.strftime('%d/%m/%Y'), format21_left_bold)
            # row += 2

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
            sheet.insert_image('A2:A4', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 50})

            # sheet.merge_range(1, 1, 3, 1, '', format_1)
            sheet.merge_range('A2:A4', '', format_1)
            title = 'EVALUACIÓN DE PROVEEDOR CRÍTICO' if evaluation.partner_id.vip_supplier else 'EVALUACIÓN DE PROVEEDOR'
            sheet.merge_range(
                'B2:E4', title, format_1)
            code = evaluation.code or ''
            sheet.merge_range('F2:G3', 'Código: ' + code, format_1)
            # sheet.merge_range(
            #     'F3:G3', 'Código: ', format_1)
            today = date.today().strftime('%d/%m/%Y')

            evaluation_date = evaluation.date_history.strftime(
                '%d/%m/%Y') if evaluation.date_history else ''
            sheet.merge_range(
                'F4:G4', 'Fecha de impresión: ' + today, format_1)

            sheet.set_row(3, 25)
            # sheet.merge_range('F4:G4', evaluation., format_1)

            sheet.write('A6', 'Fecha de evaluación', format_1)
            sheet.write('B6', evaluation_date, format21_center)

            sheet.write('C6', 'Empresa evaluada', format_1)
            sheet.write('D6', evaluation.partner_id.name, format21_center)

            sheet.write('E6', 'Responsable', format_1)
            sheet.merge_range(
                'F6:G6', evaluation.partner_id.responsible_id.name, format21_center)

            sheet.set_row(5, 25)
            sheet.set_row(6, 25)

            format21_c_bold.set_border()
            format21_left.set_border()
            format21_center.set_border()

            sheet.write(row, col, 'Puntos sobre 100', format21_c_bold)
            col += 1
            sheet.write(row, col, 'Aspecto', format21_c_bold)
            col += 1
            sheet.write(row, col, 'Puntos parciales', format21_c_bold)
            col += 1
            sheet.write(row, col, 'Criterio', format21_c_bold)
            col += 1
            sheet.write(row, col, 'Escala (1-5)', format21_c_bold)
            col += 1
            sheet.write(row, col, 'Real', format21_c_bold)
            col += 1
            sheet.write(row, col, 'Total aspecto', format21_c_bold)
            row += 1

            for item in evaluation.history_item_ids:
                col = r_col
                len_line = len(item.history_line_ids)
                if len_line == 1:
                    sheet.write(row, col, item.item_id.weight_total,
                                format21_center)
                    col += 1
                    sheet.write(row, col, item.name, format21_center)
                    col += 1
                else:
                    sheet.merge_range(
                        row, col, row+len_line-1, col, item.item_id.weight_total, format21_center)
                    col += 1
                    sheet.merge_range(row, col, row+len_line-1,
                                      col, item.name, format21_center)
                    col += 1
                col_line = col
                for line in item.history_line_ids:
                    col = col_line
                    sheet.write(row, col, line.line_id.weight, format21_center)
                    col += 1
                    sheet.write(row, col, line.name, format21_left)
                    col += 1
                    sheet.write(row, col, line.scala or 0, format21_center)
                    col += 1
                    sheet.write(row, col, line.qualification_line,
                                format21_center)
                    col += 1
                    row += 1
                if len_line == 1:
                    sheet.write(row-1, col, item.qualification_item,
                                format21_center)
                else:
                    sheet.merge_range(
                        row-1, col, row-len_line, col, item.qualification_item, format21_center)
            sheet.merge_range(row, col-2, row, col-1, "Total", format21_c_bold)
            sheet.write(row, col, evaluation.qualification, format21_c_bold)
            row += 2

            sheet.write(row, 0, 'PUNTAJE', format21_c_bold)
            sheet.write(row, 1, 'TIPO DE PROVEEDOR', format21_c_bold)
            sheet.write(row, 2, 'ACCIÓN A SEGUIR', format21_c_bold)

            sheet.write(row+1, 0, '75-100', format21_center)
            sheet.write(row+1, 1, 'MUY CONFIABLE', format21_center)
            sheet.write(
                row+1, 2, 'Enfatizar los puntos fuertes para sostener la posición, APROBADO', format21_center)

            sheet.write(
                row+2, 0, '55-74', format21_center)
            sheet.write(
                row+2, 1, 'CONDICIONAL', format21_center)
            sheet.write(
                row+2, 2, 'Realizar un seguimiento sobre todo de los puntos débiles. De no cumplir se le dará tratamiento de PROVEEDOR NO CONFIABLE.', format21_center)

            sheet.write(row+3, 0, 'Menos de 55', format21_center)
            sheet.write(row+3, 1, 'NO CONFIABLE', format21_center)
            sheet.write(row+3, 2, 'NO ACEPTABLE', format21_center)

            sheet.merge_range(row, 4, row+1, 5,
                              'CALIFICACIÓN PROVEEDOR', format21_c_bold)
            sheet.merge_range(row, 6, row+1, 6,
                              evaluation.qualification, format21_center)

            sheet.merge_range(
                row+2, 4, row+2, 5, 'Escala\n1 = Pésimo\n2 = Deficiente\n3 = Regular\n4 = Bueno\n5 = Muy bueno', format21_center)

            sheet.set_column(0, 2, 20)
            sheet.set_column(3, 3, 70)
            sheet.set_row(row, 30)
            sheet.set_row(row+1, 30)
            sheet.set_row(row+2, 80)
