import base64
import io
from collections import defaultdict

from odoo import api, fields, models
from odoo.http import request
from PIL import Image
from datetime import date


class PartnerEvaluationReport(models.AbstractModel):
    _name = 'report.stock_inspection.stock_picking_inspection_report'
    _description = 'Reporte de inspección de compras'
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

            sheet = workbook.add_worksheet('Evaluación + %s' % evaluation.inspection_date.strftime('%d%m%Y'))

            sheet.set_column(0, 0, 2)
            # sheet.set_column(1, 1, 15)
            # sheet.set_column(2, 2, 56)
            # sheet.set_column(3, 3, 15)
            # sheet.set_column(4, 6, 56)

            sheet.set_row(0, 2)
            sheet.set_column('B:F', 20)

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
            sheet.insert_image('B2:B4', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 20})
            sheet.merge_range('B2:B4', '', format_1)
            sheet.merge_range('C2:E4', 'INSPECCIÓN DE COMPRAS', format_1)
            sheet.write('F2', 'Código: ', format_1)
            sheet.write('F3', 'Versión: ', format_1)
            sheet.write('F4', 'Fecha de impresión: ', format_1)

            sheet.write('B6', 'Fecha de inspección', format_1)
            sheet.write('B7', 'Proveedor', format_1)
            sheet.write('B8', 'Documento de origen', format_1)

            sheet.write('C6', evaluation.inspection_date.strftime('%d/%m/%Y'), format21_center)
            sheet.write('C7', evaluation.picking_id.partner_id.name, format21_center)
            sheet.write('C8', evaluation.picking_id.origin, format21_center)

            sheet.write('E6', 'Responsable', format_1)
            sheet.write('E7', 'Hora', format_1)
            sheet.write('E8', 'Ubicación destino', format_1)

            sheet.write('F6', evaluation.employee_id.name, format21_center)
            sheet.write('F7', evaluation.inspection_date.strftime('%H:%m'), format21_center)
            sheet.write('F8', '', format21_center)

            sheet.merge_range('B10:C10', 'CRITERIOS', format_1)
            sheet.write('B11', 'CRITERIO', format_1)
            sheet.write('C11', 'SI/NO/NO APLICA', format_1)

            row = 11
            for cr in evaluation.item_ids:
                if cr.yes:
                    state = 'Sí'
                elif cr.no:
                    state = 'No'
                elif cr.no_apply:
                    state = 'No aplica'
                else:
                    state = ''
                sheet.write(row, 1, cr.name, format21_center)
                sheet.write(row, 2, state, format21_center)
                row+=1
            
            sheet.merge_range('E10:F10', 'Observaciones', format_1)
            sheet.merge_range('E11:F16', evaluation.observations, format21_center)

            # sheet.write(row+2, 1, 'Responsable', format_1)
            # sheet.write(row+2, 2, evaluation.employee_id.name, format_1)



            

            
