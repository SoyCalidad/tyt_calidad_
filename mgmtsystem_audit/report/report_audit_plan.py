# -*- coding: utf-8 -*-
import base64
import io
import os
import re
import time
from datetime import datetime
from io import StringIO
from PIL import Image

import lxml.html
from lxml import etree
from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class AuditPlanXLS(models.AbstractModel):
    _name = 'report.mgmtsystem_audit.report_audit_plan'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        """Generate a xls report with the data

        Arguments:
            workbook {object} -- A object that represents a Excel workbook
            data {dict} -- The data of the report
            partners {object} -- A class object

        Raises:
            UserError: When the user choose a initial balance but no a initial date
        """

        if data and data.get('is_wizard'):
            partners = self.env['audit.plan'].browse(data['ids'])
        
        format_title = workbook.add_format(
            {'font_size': 13, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'align': 'center'})
        format_data = workbook.add_format(
            {'font_size': 9, 'font_name': 'Arial'})
        format_header = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 1})
        monetary_size_8_r = workbook.add_format(
            {'num_format': '"S/." #,##0.00', 'font_size': 9, 'align': 'right', 'valign': 'vcenter', 'border': 1})
        format_1 = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 1, 'bg_color': '#EEEEEE'})
        format_2 = workbook.add_format(
            {'font_size': 9, 'font_name': 'Arial', 'valign': 'vcenter', 'text_wrap': True, 'border': 1, 'align': 'center'})
        format_3 = workbook.add_format(
            {'font_size': 9, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': 1})

        
        sheet1 = workbook.add_worksheet('PROGRAMA ANUAL DE AUDITORÍAS')
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
        sheet1.insert_image('A1', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
        sheet1.set_column("C:G", 25)

        sheet1.merge_range(0, 0, 1, 0, '', format_title)
        sheet1.merge_range(
            0, 1, 1, 4, 'PROGRAMA ANUAL DE AUDITORÍASPlan de COMUNICACIONES', format_title)
        sheet1.write(0, 5, 'MOD-PGI', format_title)
        sheet1.write(1, 5, partners.numero, format_title)
        sheet1.merge_range(2, 1, 2, 5, 'SISTEMA DE GESTIÓN', format_1)

        init_dates = [x.date_init for x in partners.audit_ids]
        end_dates = [x.date_fin for x in partners.audit_ids]
        all_dates = init_dates + end_dates
        min_date = min(all_dates)
        min_date_t = datetime.strptime(
            min_date, DEFAULT_SERVER_DATETIME_FORMAT)
        max_date = max(all_dates)
        max_date_t = datetime.strptime(
            max_date, DEFAULT_SERVER_DATETIME_FORMAT)

        min_date_month = min_date_t.month
        min_date_year = min_date_t.year
        max_date_month = max_date_t.month
        max_date_year = max_date_t.year

        # if min_date_year != max_date_year:
        #     to_end = 12 - min_date_year
        #     sheet1.merge_range(3, 0, to_end*3, 0, 'Año ' + min_date_year, format_header)
        #     for i in range(to_end):
        #         sheet1.merge_range(4, 0, 4, i*3, 'Mes ' + min_date_month, format_header)
        # else:
        sheet1 . set_row ( 3 , 30 )
        sheet1 . set_row ( 4 , 30 )
        sheet1 . set_row ( 5 , 30 )
        sheet1 . set_row ( 6 , 30 )
        sheet1 . set_row ( 7 , 30 )
        sheet1 . set_row ( 8 , 30 )
        sheet1.merge_range(3, 1, 3, 2, 'Nombre', format_header)
        sheet1.merge_range(4, 1, 4, 2, 'Tipo', format_header)
        sheet1.merge_range(5, 1, 5, 2, 'Alcance', format_header)
        sheet1.merge_range(6, 1, 6, 2, 'Fecha de inicio', format_header)
        sheet1.merge_range(7, 1, 7, 2, 'Fecha de fin', format_header)
        sheet1.merge_range(8, 1, 8, 2, 'Duración', format_header)

        for i, line in enumerate(partners.audit_ids, start=3):
            
            sheet1.write(3, i, line.name, format_2)
            sheet1.write(4, i, line.type, format_2)
            sheet1.write(5, i, line.observations, format_2)
            sheet1.write(6, i, line.date_init, format_2)
            sheet1.write(7, i, line.date_fin, format_2)
            sheet1.write(8, i, line.duration, format_2)

        workbook.close()
