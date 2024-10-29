
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

class NonConformityReportWizard(models.TransientModel):
    _name = 'non.conformity.output.wizard'
    _description = 'Control of non-conforming outputs'

    start_date = fields.Date(string="Start Date", default=fields.Date.context_today, required=True)
    end_date = fields.Date(string="End Date", default=fields.Date.context_today, required=True)
    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', 
        string='Nonconformities', 
        domain='[("nc_output", "=", True)]'
    )

    def generate_report(self):
        self.ensure_one()
        if self.start_date > self.end_date:
            raise UserError("The Start Date must be less than the End Date.")
        
        nonconformity_ids = self.nonconformity_ids if self.nonconformity_ids else self.env['mgmtsystem.nonconformity'].search([
            ('nc_output', '=', True),
            ('create_date', '>=', self.start_date),
            ('create_date', '<=', self.end_date),
        ])

        if not nonconformity_ids:
            raise UserError("No records found within the specified dates.")
        
        return self.env.ref('tyt_non_conforming_outputs.report_nco_xlsx').report_action(nonconformity_ids)


class NonConformityOutputXlsxReport(models.AbstractModel):
    _name = 'report.report_excel_nco_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Control of non-conforming outputs'

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
			'bg_color': '#a5a5a5','border': 2,
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
            'Control of non-conforming outputs',)
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
        sheet.set_column('B:B', 20) 
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 30) 
        sheet.set_column('F:F', 60)
        sheet.set_column('G:G', 60)
        sheet.set_column('H:H', 60) 

        model_id = self.env['ir.model'].search(
            [('model', '=', self._name)],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)
        code = code.code if code else ''
        sheet.merge_range('B2:C5', '', format21_c_bold)
        sheet.merge_range(
            'D2:G5', 'CONTROL DE SALIDAS NO CONFORMES', format26_c_bold)
        
        
        sheet.merge_range('B7:B8', 'Fecha', format21_gray_bold)
        sheet.merge_range('C7:C8', 'Cliente-proyecto-plaza', format21_gray_bold)
        sheet.merge_range('D7:D8', 'No conformidad', format21_gray_bold)
        sheet.merge_range('E7:E8', 'Penalización relacionada', format21_gray_bold)
        sheet.merge_range('F7:F8', 'Acciones tomadas', format21_gray_bold)
        sheet.merge_range('G7:G8', 'Negociación de penalizaciones con clientes', format21_gray_bold)
        sheet.merge_range('H7:H8', 'Autoridad que decide la acción con respecto a la no conformidad', format21_gray_bold)
       

        row = 8
        for record in records:
            sheet.write(row, 1, record.nc_create_date or '', format21_date_center)
            sheet.write(row, 2, record.client_id.name or '', format21_justify)
            sheet.write(row, 3, record.name or '', format21_justify)
            
            penalties = "\n".join([f"• {penalty.name}" for penalty in record.penalty_ids]) or ''
            sheet.write(row, 4, penalties, format21_justify)
            
            actions = "\n".join([f"• {action.name}" for action in record.action_ids]) or ''
            sheet.write(row, 5, actions , format21_justify)
            
            sheet.write(row, 6, record.penalty_negotiation_clients or '', format21_justify) 
            
            actions_r = "\n".join([f"• {action.user_id.name}" for action in record.action_ids]) or ''
            sheet.write(row, 7, actions_r , format21_justify)
            row += 1
           