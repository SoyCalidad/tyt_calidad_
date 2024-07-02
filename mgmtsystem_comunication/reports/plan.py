# -*- coding: utf-8 -*-
import base64
import io
import os
import re
import time
from datetime import datetime
from io import StringIO
from math import ceil

import lxml.html
from lxml import etree
from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from PIL import Image


class ComunicationPlanXLS(models.AbstractModel):
    _name = 'report.mgmtsystem_comunication.report_comunication_plan'
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

        format_title = workbook.add_format(
            {'font_size': 13, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'align': 'center', 'bg_color': '#EEEEEE', 'border': 1})
        format_1 = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 1, 'bg_color': '#EEEEEE'})
        format_2 = workbook.add_format(
            {'font_size': 9, 'font_name': 'Arial', 'valign': 'vcenter', 'text_wrap': True, 'border': 1, 'align': 'center'})

        company = self.env.user.company_id

        sheet1 = workbook.add_worksheet('Programa de comunicaciones')

        if data.get('is_wizard'):
            partners = self.env['comunication.plan'].browse(data['docs'])

        # Main
        sheet1.set_column('B:B', 50)
        sheet1.set_column('C:H', 20)
        sheet1.set_column('G:G', 35)

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
        sheet1.insert_image('B2:B4', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 150})

        sheet1.merge_range(1, 1, 3, 1, '', format_1)
        sheet1.merge_range('B2:B4', '', format_title)

        sheet1.merge_range(
            'C2:E4', partners.name, format_title)
        code = partners.code or ''
        sheet1.merge_range('F2:G2', 'Código: ' + code, format_1)
        version = str(partners.version) or ''
        sheet1.merge_range('F3:G3', 'Versión: ' + version, format_1)
        date_validate = partners.date_validate.strftime(
            '%d/%m/%Y') if partners.date_validate else ''
        sheet1.merge_range(
            'F4:G4', 'Fecha de validación: ' + date_validate, format_1)

        entrie_row = 6
        sheet1.merge_range(
            4, 1, 4, 6, 'COMUNICACIONES INTERNAS', format_1)
        sheet1.merge_range(5, 1, 5, 2, 'QUE SE COMUNICA', format_1)
        sheet1.write(5, 3, 'CUANDO', format_1)
        sheet1.write(5, 4, 'A QUIÉN', format_1)
        sheet1.write(5, 5, 'COMO', format_1)
        sheet1.write(5, 6, 'QUIÉN COMUNICA', format_1)

        max_internal_height = 10
        for each in partners.line_ids:
            if each.type in ('interna', 'both'):
                if each.employee_ids:
                    resume = each.resume or ''
                    date_release = each.date_release.strftime(
                        '%d/%m/%Y') if each.date_release else ''
                    employees = ', '.join([x.name for x in each.employee_ids])
                    via = each.via or ''
                    user_id = each.user_id.name if each.user_id else ''
                    sheet1.set_row(entrie_row, 30)
                    sheet1.merge_range(
                        entrie_row, 1, entrie_row, 2, resume, format_2)
                    sheet1.write(entrie_row, 3, date_release, format_2)
                    sheet1.write(entrie_row, 4, employees, format_2)
                    sheet1.write(entrie_row, 5, via, format_2)
                    sheet1.write(entrie_row, 6, user_id, format_2)
                    max_len = max(len(resume), len(employees), len(via))
                    if max_len > 20:
                        max_internal_height = ceil(max_len/20)*10
                    sheet1.set_row(entrie_row, max_internal_height)
                    entrie_row += 1

        entrie_row += 1
        sheet1.merge_range(entrie_row, 1, entrie_row, 6,
                           'COMUNICACIONES EXTERNAS', format_1)
        entrie_row += 1
        sheet1.merge_range(entrie_row, 1, entrie_row, 2,
                           'QUE SE COMUNICA', format_1)
        sheet1.write(entrie_row, 3, 'CUANDO', format_1)
        sheet1.write(entrie_row, 4, 'A QUIÉN', format_1)
        sheet1.write(entrie_row, 5, 'COMO', format_1)
        sheet1.write(entrie_row, 6, 'QUIÉN COMUNICA', format_1)
        entrie_row += 1

        max_external_height = 10
        for each in partners.line_ids:
            if each.type in ('externa', 'both'):
                if each.partner_ids:
                    resume = each.resume or ''
                    date_release = each.date_release.strftime(
                        '%d/%m/%Y') if each.date_release else ''
                    partner = ', '.join(
                        [x.name for x in each.partner_ids]) if each.partner_ids else ''
                    via = each.via or ''
                    user_id = each.user_id.name if each.user_id else ''
                    sheet1.merge_range(
                        entrie_row, 1, entrie_row, 2, resume, format_2)
                    sheet1.write(entrie_row, 3, date_release, format_2)
                    sheet1.write(entrie_row, 4, partner, format_2)
                    sheet1.write(entrie_row, 5, via, format_2)
                    sheet1.write(entrie_row, 6, user_id, format_2)
                    max_len = max(len(resume), len(employees), len(via))
                    if max_len > 20:
                        max_external_height = ceil(max_len/20)*10
                    sheet1.set_row(entrie_row, max_external_height)
                    entrie_row += 1
                    entrie_row += 1

        workbook.close()
