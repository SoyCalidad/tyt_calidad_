
import base64
import io
from PIL import Image
from odoo import models

from collections import defaultdict
import pytz
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from odoo import models, fields, api
from odoo.exceptions import UserError

class NonConformityLogWizard(models.TransientModel):
    _name = 'non.conformity.log.wizard'
    _description = 'Log of non-conforming products'

    start_date = fields.Date(string="Start Date", default=fields.Date.context_today, required=True)
    end_date = fields.Date(string="End Date", default=fields.Date.context_today, required=True)
    nonconformity_ids = fields.Many2many(
        'non.conforming.products.log', 
        string='Non Conformities Log', 
    )

    def generate_report(self):
        self.ensure_one()
        if self.start_date > self.end_date:
            raise UserError("The Start Date must be less than the End Date.")
        
        nonconformity_ids = self.nonconformity_ids if self.nonconformity_ids else self.env['non.conforming.products.log'].search([
            ('create_date', '>=', self.start_date),
            ('create_date', '<=', self.end_date),
        ])

        if not nonconformity_ids:
            raise UserError("No records found within the specified dates.")
        
        return self.env.ref('tyt_non_conforming_products_log.report_ncolog_xlsx').report_action(nonconformity_ids)


class NonConformityOutputXlsxReport(models.AbstractModel):
    _name = 'report.report_excel_ncolog_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Log of non-conforming products'

    def generate_xlsx_report(self, workbook, data, records):
        format21_c_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EFEFEF', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
        format21_gray = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        format21_gray_bold = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True,'font_color': 'white',
			'bg_color': '#31879b','border': 2,
			'text_wrap': True,
			'border_color': '#757070', })
        format21_gray_bold_g = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True,
			'bg_color': '#757070','border': 2,
			'text_wrap': True,
			'border_color': '#757070', })
        format21_gray_bold_sb = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True,
			'bg_color': '#b7dee8','border': 2,
			'text_wrap': True,
			'border_color': '#757070', })
        format26_c_bold = workbook.add_format(
            {'font_size': 26, 'font_color': 'white',
			'bg_color': '#31879b','border': 2,
			'border_color': '#757070', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_date_center = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'num_format': 'dd/mm/yyyy'}
        )
        format21_justify = workbook.add_format(
            {'font_size': 10, 'align': 'justify', 'valign': 'vcenter', 'bold': False, 'text_wrap': True}
        )
        number = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'num_format': '#,##0'})
        format_number = workbook.add_format(
        {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'num_format': '#,##0.00'})


        sheet = workbook.add_worksheet(
            'Log of non-conforming products',)
        sheet.hide_gridlines(option=2)
        company_id = self.env.user.company_id

        buf_image = io.BytesIO(base64.b64decode(company_id.logo))
        im = Image.open(buf_image)
        width, height = im.size
        image_width = width
        image_height = height
        cell_width = 80
        cell_height = 60

        x_scale = cell_width/image_width
        y_scale = cell_height/image_height
        sheet.insert_image('B2:B3', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 25})
        
        sheet.set_column('A:A', 15) 
        sheet.set_column('B:N', 30)
        sheet.set_column('O:S', 20)
        sheet.set_column('T:AS', 25)

        model_id = self.env['ir.model'].search(
            [('model', '=', self._name)],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code else ''
        sheet.merge_range('B2:C5', '', format21_c_bold)
        sheet.merge_range(
            'D2:G5', 'BITACORA PRODUCTOS DE NO CONFORMES', format26_c_bold)
        
        sheet.merge_range('B9:B10', 'SITIO', format21_gray_bold)
        sheet.merge_range('C9:C10', 'ID DE REPORTE', format21_gray_bold)
        sheet.merge_range('D9:D10', 'CAMPAÑA', format21_gray_bold)
        sheet.merge_range('E9:E10', 'FECHA DE REPORTE', format21_gray_bold)
        sheet.merge_range('F9:F10', 'NÚMERO DE LA LÍNEA', format21_gray_bold)
        sheet.merge_range('G9:G10', 'LOGIN', format21_gray_bold)
        sheet.merge_range('H9:H10', 'NOMBRE COMPLETO', format21_gray_bold)
        sheet.merge_range('I9:I10', 'MOTIVO DE AJUSTE (PNC)', format21_gray_bold)
        sheet.merge_range('J9:J10', 'FECHA DE VALIDACIÓN', format21_gray_bold)
        sheet.merge_range('K9:K10', 'PROCEDE / NO PROCEDE', format21_gray_bold)
        sheet.merge_range('L9:L10', 'RESPONSABLE DE PNC', format21_gray_bold)
        sheet.merge_range('M9:M10', 'AJUSTE FIRMADO', format21_gray_bold)
        sheet.merge_range('N9:N10', 'MONTO GENERAL', format21_gray_bold)

        sheet.merge_range('O9:Q9', 'Descuento', format21_gray_bold)

        sheet.write('O10', 'SEMANAS NOMINALES (Descuento)', format21_gray_bold_g)
        sheet.write('P10', 'FECHA INICIO', format21_gray_bold_g)
        sheet.write('Q10', 'FECHA FINAL', format21_gray_bold_g)
    
        sheet.merge_range('R9:R10', 'MONTO x SEM', format21_gray_bold)
        sheet.merge_range('S9:S10', 'FRECUENCIA', format21_gray_bold)
        
        
        # Primer Pago
        sheet.merge_range('T8:X8', 'PRIMER PAGO', format21_gray_bold)
        sheet.merge_range('T9:T10', 'FOLIO TICKET', format21_gray_bold)
        sheet.merge_range('U9:U10', 'FECHA DE PAGO DE PNC', format21_gray_bold_sb)
        sheet.merge_range('V9:V10', 'MONTO DEL PAGO', format21_gray_bold_sb)
        sheet.merge_range('W9:W10', 'ESTATUS', format21_gray_bold_g)
        sheet.merge_range('X9:X10', 'APLICA DESCUENTO A', format21_gray_bold_sb)

        # Segundo Pago
        sheet.merge_range('Y8:AC8', 'SEGUNDO PAGO', format21_gray_bold)
        sheet.merge_range('Y9:Y10', 'FOLIO TICKET', format21_gray_bold)
        sheet.merge_range('Z9:Z10', 'FECHA DE PAGO DE PNC', format21_gray_bold_sb)
        sheet.merge_range('AA9:AA10', 'MONTO DEL PAGO', format21_gray_bold_sb)
        sheet.merge_range('AB9:AB10', 'ESTATUS', format21_gray_bold_g)
        sheet.merge_range('AC9:AC10', 'APLICA DESCUENTO A', format21_gray_bold_sb)

        # Tercer Pago
        sheet.merge_range('AD8:AH8', 'TERCER PAGO', format21_gray_bold)
        sheet.merge_range('AD9:AD10', 'FOLIO TICKET', format21_gray_bold)
        sheet.merge_range('AE9:AE10', 'FECHA DE PAGO DE PNC', format21_gray_bold_sb)
        sheet.merge_range('AF9:AF10', 'MONTO DEL PAGO', format21_gray_bold_sb)
        sheet.merge_range('AG9:AG10', 'ESTATUS', format21_gray_bold_g)
        sheet.merge_range('AH9:AH10', 'APLICA DESCUENTO A', format21_gray_bold_sb)

        # Cuarto Pago
        sheet.merge_range('AI8:AM8', 'CUARTO PAGO', format21_gray_bold)
        sheet.merge_range('AI9:AI10', 'FOLIO TICKET', format21_gray_bold)
        sheet.merge_range('AJ9:AJ10', 'FECHA DE PAGO DE PNC', format21_gray_bold_sb)
        sheet.merge_range('AK9:AK10', 'MONTO DEL PAGO', format21_gray_bold_sb)
        sheet.merge_range('AL9:AL10', 'ESTATUS', format21_gray_bold_g)
        sheet.merge_range('AM9:AM10', 'APLICA DESCUENTO A', format21_gray_bold_sb)

        # Quinto Pago
        sheet.merge_range('AN8:AR8', 'QUINTO PAGO', format21_gray_bold)
        sheet.merge_range('AN9:AN10', 'FOLIO TICKET', format21_gray_bold)
        sheet.merge_range('AO9:AO10', 'FECHA DE PAGO DE PNC', format21_gray_bold_sb)
        sheet.merge_range('AP9:AP10', 'MONTO DEL PAGO', format21_gray_bold_sb)
        sheet.merge_range('AQ9:AQ10', 'ESTATUS', format21_gray_bold_g)
        sheet.merge_range('AR9:AR10', 'APLICA DESCUENTO A', format21_gray_bold_sb)


        sheet.merge_range('AS9:AS10', 'COMENTARIOS', format21_gray_bold)

        row = 9
        for record in records:
            row += 1
            sheet.write(row, 1, record.site.name or '', format21_left)  # Columna B
            sheet.write(row, 2, record.report_id or '', format21_left)  # Columna C
            sheet.write(row, 3, record.campaign.name or '', format21_left)  # Columna D
            sheet.write(row, 4, record.report_date or '', format21_date_center)  # Columna E
            sheet.write(row, 5, record.line_number or '', number)  # Columna F
            sheet.write(row, 6, record.login or '', format21_left)  # Columna G
            sheet.write(row, 7, record.complete_name.name or '', format21_left)  # Columna H
            sheet.write(row, 8, record.adjustment_cause or '', format21_left)  # Columna I
            sheet.write(row, 9, record.validation_date or '', format21_date_center)  # Columna J
            sheet.write(row, 10, 'APLICA' if record.proceed else 'NO APLICA', format21_left)  # Columna K
            sheet.write(row, 11, record.pnc_responsable.name or '', format21_left)  # Columna L
            sheet.write(row, 12, 'SÌ' if record.signed_adjustment else 'NO', format21_left)  # Columna M
            sheet.write(row, 13, record.general_amount or 0, format_number)  # Columna N
            sheet.write(row, 14, record.nominal_weeks or '', format21_left)  # Columna O
            sheet.write(row, 15, record.start_date or '', format21_date_center)  # Columna P
            sheet.write(row, 16, record.end_date or '', format21_date_center)  # Columna Q
            
            sheet.write(row, 17, record.weekly_amount or '', format_number)  # Columna R
            sheet.write(row, 18, record.frequency.name or '', format21_left)  # Columna S
            
            
            # Campos de pagos (5 pagos)
            col_start = 19  # Columna T para Primer Pago
            for payment in record.payments_ids:
                sheet.write(row, col_start, payment.folio or '', format21_left)  # Columna FOLIO TICKET
                sheet.write(row, col_start + 1, payment.date or '', format21_date_center)  # Columna FECHA DE PAGO DE PNC
                sheet.write(row, col_start + 2, payment.amount or 0, format21_left)  # Columna MONTO DEL PAGO
                sheet.write(row, col_start + 3, 'Pagado' if payment.paymeny_status == 'pagado' else 'No Pagado', format21_left)  # Columna ESTATUS
                sheet.write(row, col_start + 4, payment.responsable.name or '', format21_left)  # Columna APLICA DESCUENTO A
                col_start += 5  # Avanza a las columnas del siguiente pago

            # Comentarios
            sheet.write(row, 44, record.coments or '', format21_left)  # Columna AS

        