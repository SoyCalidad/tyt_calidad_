import base64
import io
from collections import defaultdict

from odoo import api, fields, models
from odoo.http import request
from PIL import Image
from datetime import date


class PartnerInitialEvaluationReport(models.AbstractModel):
    _name = 'report.mgmtsystem_partner_qualification.r_initial_evaluation'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, evaluations):
        format21_c_bold = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'bg_color': '#A0A0A0', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_left_bold = workbook.add_format(
            {'font_size': 10, 'align': 'left', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'left', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
        format21_center = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 1})
        format_1 = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 1, 'bg_color': '#EEEEEE'})
        format_title = workbook.add_format(
            {'font_size': 13, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'align': 'center', 'bg_color': '#EEEEEE', 'border': 1})

        if data and data.get('is_wizard'):
            evaluations = self.env['res.partner.evaluation.history'].browse(
                data['ids'])

        for evaluation in evaluations:
            initial_evaluation_date = evaluation.initial_evaluation_date.strftime(
                '%d-%m-%Y') if evaluation.initial_evaluation_date else ''
            sheet = workbook.add_worksheet(
                'Evaluación + %s' % initial_evaluation_date)

            sheet.set_column(0, 0, 2)
            # sheet.set_column(1, 1, 15)
            # sheet.set_column(2, 2, 56)
            # sheet.set_column(3, 3, 15)
            # sheet.set_column(4, 6, 56)

            sheet.set_row(0, 2)
            sheet.set_column('B:F', 20)

            company_id = self.env.user.company_id
            today = date.today().strftime('%d/%m/%Y')
            val_date = evaluation.initial_evaluation_id.date_validate
            val_date_str = val_date.strftime('%d/%m/%Y') if val_date else ''

            buf_image = io.BytesIO(base64.b64decode(company_id.logo))
            im = Image.open(buf_image)
            width, height = im.size
            image_width = width
            image_height = height
            cell_width = 48.0
            cell_height = 48.0

            x_scale = cell_width/image_width
            y_scale = cell_height/image_height
            sheet.insert_image('B2:B4', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 55, 'y_offset': 10})
            sheet.merge_range('B2:B4', '', format_1)
            sheet.merge_range('C2:E4', 'FICHA DE PROVEEDOR', format_1)
            code = evaluation.code or ''
            sheet.merge_range('F2:F3', 'Código: ' + code, format_1)
            sheet.write('F4', 'Fecha de validación: ' + val_date_str, format_1)

            sheet.set_row(3, 25)
            sheet.set_row(4, 0)

            sheet.write('B6', 'Fecha', format_1)
            initial_evaluation_date = evaluation.initial_evaluation_date.strftime(
                '%d/%m/%Y') if evaluation.initial_evaluation_date else ''
            sheet.write('C6', initial_evaluation_date, format21_center)

            sheet.write('D6', 'Evaluador', format_1)
            sheet.merge_range(
                'E6:F6', evaluation.employee_id.name, format21_center)

            sheet.merge_range('B7:F7', 'DATOS GENERALES', format_1)

            sheet.merge_range('B8:C8', 'RUC*:', format_1)
            sheet.merge_range(
                'D8:F8', evaluation.partner_id.vat, format21_center)

            sheet.merge_range('B9:C9', 'RAZÓN SOCIAL:', format_1)
            sheet.merge_range(
                'D9:F9', evaluation.partner_id.name, format21_center)

            contact_address = evaluation.partner_id.contact_address if evaluation.partner_id and evaluation.partner_id.contact_address else ''

            sheet.merge_range('B10:C10', 'DIRECCIÓN:', format_1)
            sheet.merge_range('D10:F10', contact_address.strip(
            ).replace('\n', ', '), format21_center)

            sheet.set_row(9, 17)

            contact = ''
            for child in evaluation.partner_id.child_ids:
                if child.type == 'contact':
                    contact = child.name
                    break
            sheet.merge_range('B11:C11', 'CONTACTO:', format_1)
            sheet.write('D11', contact, format21_center)

            sheet.write('E11', 'TELÉFONO:', format_1)
            sheet.write('F11', evaluation.partner_id.phone, format21_center)

            sheet.merge_range('B12:C12', 'E-MAIL:', format_1)
            sheet.merge_range(
                'D12:F12', evaluation.partner_id.email, format21_center)

            sheet.merge_range('B13:C13', 'PRODUCTOS Y SERVICIOS:', format_1)
            sheet.merge_range('D13:F13', ','.join(
                [x.name for x in evaluation.partner_id.product_ids]), format21_center)

            sheet.merge_range('B14:F14', 'CRITERIOS', format_1)

            sheet.write('B15', 'ÍTEM', format_1)
            sheet.merge_range('C15:D15', 'CRITERIO', format_1)
            sheet.write('E15', 'SÍ', format_1)
            sheet.write('F15', 'NO', format_1)

            row = 15
            for i, cr in enumerate(evaluation.item_ids, 1):
                if cr.yes:
                    state = 'Sí'
                elif cr.no:
                    state = 'No'
                else:
                    state = ''
                sheet.write(row, 1, i, format21_center)
                sheet.merge_range(row, 2, row, 3, cr.name, format21_center)
                sheet.write(row, 4, 'X' if state ==
                            'Sí' else '', format21_center)
                sheet.write(row, 5, 'X' if state ==
                            'No' else '', format21_center)
                sheet.set_row(row, 25)
                row += 1

            sheet.merge_range(row, 1, row+1, 1,
                              'RESULTADO DE LA EVALUACIÓN', format_1)
            sheet.merge_range(row, 2, row, 5,
                              'PROVEEDOR SELECCIONADO', format_1)
            sheet.write(row+1, 2, 'SÍ', format_1)
            sheet.write(
                row+1, 3, 'X' if evaluation.select_yes else '', format21_center)
            sheet.write(row+1, 4, 'NO', format_1)
            sheet.write(
                row+1, 5, 'X' if evaluation.select_no else '', format21_center)

            sheet.merge_range(row+2, 1, row+2, 5, 'OBSERVACIONES', format_1)
            sheet.merge_range(row+3, 1, row+6, 5,
                              evaluation.observations, format21_center)

            sheet.merge_range(row+7, 1, row+7, 5,
                              'CRITERIO DE EVALUACIÓN', format_1)
            sheet.merge_range(row+8, 1, row+8, 5,
                              evaluation.final_criteria, format21_center)

            sheet.set_row(row+8, 50)

            sheet.set_column(1, 5, 17)
