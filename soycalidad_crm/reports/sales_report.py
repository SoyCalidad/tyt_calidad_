# -*- coding: utf-8 -*-
import base64
import io
from collections import defaultdict
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from PIL import Image


class SalesResume(models.TransientModel):
    _name = 'sale.order.resume_report'
    _description = 'Reporte de ventas'

    user_id = fields.Many2many('res.users', string='Ejecutivo comercial')
    init_date = fields.Datetime(string='De')
    end_date = fields.Datetime(string='A')

    def action_print(self):
        names = [x.name for x in self.user_id]
        init_date = self.init_date.strftime('%d/%m/%Y') if self.init_date else ''
        end_date = self.end_date.strftime('%d/%m/%Y') if self.end_date else ''
        datas = {
            'user_id': names,
            'init_date': self.init_date,
            'end_date': self.end_date,
        }
        sales = self.env['sale.order'].search([('user_id', 'in', self.user_id.ids), (
            'date_order', '>=', self.init_date), ('date_order', '<=', self.end_date)])
        return self.env.ref('soycalidad_crm.action_report_sales_resume').report_action(sales, data=datas)


class SalesResumeReport(models.AbstractModel):
    _name = 'report.soycalidad_crm.sales_resume'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, sales):
        try:
            sheet = workbook.add_worksheet(
                'Reporte de ventas')

            format21_c_bold = workbook.add_format(
                {'font_size': 8, 'bg_color': '#c0c0c0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': True})
            format21_gray = workbook.add_format(
                {'font_size': 10, 'bg_color': '#c0c0c0', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
            format21_row = workbook.add_format(
                {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
            format26_c_bold = workbook.add_format(
                {'font_size': 26, 'bg_color': '#c0c0c0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': True})

            company_id = self.env.user.company_id

            buf_image = io.BytesIO(base64.b64decode(company_id.logo))
            im = Image.open(buf_image)
            width, height = im.size
            image_width = width
            image_height = height
            cell_width = 40
            cell_height = 40

            x_scale = cell_width/image_width
            y_scale = cell_height/image_height
            sheet.insert_image('A1', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 10})
            sheet.merge_range(
                'B1:G2', 'REPORTE DE VENTAS', format26_c_bold)
            sheet.merge_range('H1:I1', 'Código: ', format21_c_bold)
            sheet.merge_range('H2:I2', 'Edición:', format21_c_bold)

            sheet.merge_range(
                2, 0, 2, 2, 'EJECUTIVO COMERCIAL', format21_c_bold)
            sheet.merge_range(2, 3, 2, 4, '', format21_c_bold)

            sheet.write(2, 5, 'FECHA DE INICIO', format21_c_bold)
            init_date = data['init_date']
            sheet.write(2, 6, init_date, format21_c_bold)

            sheet.write(2, 7, 'FECHA FIN', format21_c_bold)
            end_date = data['end_date']
            sheet.write(2, 8, end_date, format21_c_bold)

            sheet.write(3, 0, 'N°', format21_c_bold)
            sheet.write(3, 1, 'EJECUTIVO COMERCIAL', format21_c_bold)
            sheet.write(3, 2, 'CLIENTE', format21_c_bold)
            sheet.write(3, 3, 'CORREO', format21_c_bold)
            sheet.write(3, 4, 'NÚMERO', format21_c_bold)
            sheet.write(3, 5, 'CÓDIGO DE COTIZACIÓN', format21_c_bold)
            sheet.write(3, 6, 'PRODUCTO/SERVICIO', format21_c_bold)
            sheet.write(3, 7, 'PRECIO', format21_c_bold)
            sheet.write(3, 8, 'ESTADO', format21_c_bold)

            sheet.set_row(3, 20)
            sheet.set_column('A:A', 10)
            sheet.set_column('B:I', 30)

            for i, sale in enumerate(sales, 4):
                products = '\n'.join([x.name for x in sale.order_line])
                sheet.set_row(i, len(products))
                sheet.write(i, 0, i-3, format21_row)
                sheet.write(i, 1, sale.user_id.name, format21_row)
                sheet.write(i, 2, sale.partner_id.name, format21_row)
                sheet.write(i, 3, sale.partner_id.email, format21_row)
                sheet.write(i, 4, sale.partner_id.phone, format21_row)
                sheet.write(i, 5, sale.name, format21_row)
                sheet.write(i, 6, products, format21_row)
                sheet.write(i, 7, sale.amount_total, format21_row)
                sheet.write(i, 8, dict(sale._fields['state'].selection).get(
                    sale.state), format21_row)

        except:
            raise UserError("Hubo un error al generar el reporte")
