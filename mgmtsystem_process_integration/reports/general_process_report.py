# -*- coding: utf-8 -*-
import base64
import io
import os
import time
from datetime import datetime
from PIL import Image
import math

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class GeneralProcessReport(models.AbstractModel):
    _name = 'report.mgmtsystem_process_integration.general_process_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        """Genera el reporte de procesos"""

        format_title = workbook.add_format(
            {'font_size': 13, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'align': 'center', 'border': True, 'bg_color': '#EEEEEE'})
        format_data = workbook.add_format(
            {'font_size': 9, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'border': True, 'text_wrap': True})
        format_header = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'border': True, 'text_wrap': True, 'bold': True, 'align': 'center', 'bg_color': '#EEEEEE'})
        format_text = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'border': True, 'align': 'center', 'text_wrap': True, 'valign': 'vcenter'})

        partners_ = partners
        partners = ''

        for partners in partners_:
            sheet = workbook.add_worksheet('%s' % partners.name)
            sheet.set_column('A:B', 30)
            sheet.set_column('C:F', 15)
            sheet.set_column('G:H', 30)

            sheet.set_row(8, 20)

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
            sheet.insert_image('A1', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
            sheet.merge_range('B1:F3', 'Ficha de proceso', format_title)
            code = partners.code if partners.code else ''
            sheet.write('G1:G1', 'Codigo:', format_header)
            sheet.write('G2:G2', 'Versión:', format_header)
            sheet.write('G3:G3', 'Fecha de validación:', format_header)
            sheet.write(
                'H1:H1', partners.code, format_data)
            create_date = partners.create_date.strftime(
                '%d/%m/%Y') if partners.create_date else ''
            sheet.write(
                'H2:H2', partners.version, format_data)
            date_validate = partners.date_validate.strftime(
                '%d/%m/%Y') if partners.date_validate else ''
            sheet.write(
                'H3:H3', date_validate, format_data)

            sheet.merge_range('A4:A5', 'CÓDIGO DEL PROCESO:', format_header)
            sheet.merge_range('B4:D5', partners.code, format_text)

            sheet.merge_range(
                'E4:E5', 'NOMBRE DEL PROCESO:', format_header)
            sheet.merge_range('F4:H5', partners.name, format_text)

            sheet.merge_range('A6:A7', 'TIPO DE PROCESO', format_header)
            sheet.merge_range('B6:D7', partners.type.name, format_text)

            sheet.merge_range('E6:E7', 'DESCRIPCIÓN', format_header)
            sheet.merge_range(
                'F6:H7', partners.description, format_text)

            entrie_row = 7
            sheet.merge_range(entrie_row, 0, entrie_row,
                              7, 'PROCESO', format_header)
            entrie_row += 1
            sheet.merge_range(entrie_row, 0, entrie_row+1, 0,
                              'PROVEEDOR', format_header)
            sheet.merge_range(entrie_row, 1, entrie_row+1, 1,
                              'ENTRADA', format_header)
            sheet.merge_range(entrie_row, 2, entrie_row, 5,
                              'ACTIVIDAD', format_header)
            sheet.write(entrie_row+1, 2, 'PLANEAR', format_header)
            sheet.write(entrie_row+1, 3, 'HACER', format_header)
            sheet.write(entrie_row+1, 4, 'VERIFICAR', format_header)
            sheet.write(entrie_row+1, 5, 'ACTUAR', format_header)
            sheet.merge_range(entrie_row, 6, entrie_row+1,
                              6, 'SALIDA', format_header)
            sheet.merge_range(entrie_row, 7, entrie_row+1,
                              7, 'CLIENTE', format_header)
            entrie_row += 1

            row_real = entrie_row
            row = row_real
            len_in = len(partners.process_line_in_ids)
            len_plan = len(partners.interaction_plan)
            len_ver = len(partners.interaction_verify)
            len_do = len(partners.interaction_do)
            len_act = len(partners.interaction_act)
            len_out = len(partners.process_line_out_ids)
            lens = [len_in, len_plan, len_do, len_ver, len_act, len_out]

            max_ = max(lens)
            diff = []
            for l in lens:
                diff.append(max_-l)

            row_real = 10
            row = row_real

            def difference(le):
                if le == 0:
                    co = 1
                    re = 0
                else:
                    co = max_ / le
                    re = max_ % le
                difff = max_ - le
                if difff != 0:
                    if co >= 2:
                        if re == 0:
                            list_ = [int(co)] * le
                        else:
                            co = math.floor(co)
                            list_ = ([co+1] * int(re)) + ([co] * (le - re))
                    else:
                        list_ = ([2] * re) + ([1] * (le-re))
                else:
                    list_ = [1] * le

                return list_

            max_len = [0] * max_
            print(max_len)
            height = 20

            line_in = partners.process_line_in_ids if partners.process_line_in_ids else [
                '-']
            for i, el in enumerate(difference(len_in)):
                a = el - 1
                suppliers = ', '.join(
                    [x.name for x in line_in[i].supplier_id])
                inputs = ', '.join([x.name for x in line_in[i].input_id])

                if a == 0:
                    sheet.write(
                        row, 0, suppliers, format_data)
                    sheet.write(
                        row, 1, inputs, format_data)
                else:
                    sheet.merge_range(
                        row, 0, row+a, 0, suppliers, format_data)
                    sheet.merge_range(
                        row, 1, row+a, 1, inputs, format_data)
                row = row + a + 1
                local_max = max(len(suppliers), len(inputs))
                print(i)
                if local_max > max_len[i]:
                    max_len[i] = local_max

            row = row_real
            line_in = partners.interaction_plan if partners.interaction_plan else [
                '-']
            for i, el in enumerate(difference(len_plan)):
                a = el - 1
                if a == 0:
                    sheet.write(row, 2, line_in[i].name, format_data)
                else:
                    sheet.merge_range(row, 2, row+a, 2,
                                      line_in[i].name, format_data)
                row = row + a + 1
                local_max = len(line_in[i].name)
                if local_max > max_len[i]:
                    max_len[i] = local_max

            row = row_real
            line_in = partners.interaction_do if partners.interaction_do else [
                '-']
            for i, el in enumerate(difference(len_do)):
                a = el - 1
                if a == 0:
                    sheet.write(row, 3, line_in[i].name, format_data)
                else:
                    sheet.merge_range(row, 3, row+a, 3,
                                      line_in[i].name, format_data)
                row = row + a + 1
                local_max = len(line_in[i].name)
                if local_max > max_len[i]:
                    max_len[i] = local_max

            row = row_real
            line_in = partners.interaction_verify if partners.interaction_verify else [
                '-']
            for i, el in enumerate(difference(len_ver)):
                a = el - 1
                if a == 0:
                    sheet.write(row, 4, line_in[i].name, format_data)
                else:
                    sheet.merge_range(row, 4, row+a, 4,
                                      line_in[i].name, format_data)
                row = row + a + 1
                local_max = len(line_in[i].name)
                if local_max > max_len[i]:
                    max_len[i] = local_max

            row = row_real
            line_in = partners.interaction_act if partners.interaction_act else [
                '-']
            for i, el in enumerate(difference(len_act)):
                a = el - 1
                if a == 0:
                    sheet.write(row, 5, line_in[i].name, format_data)
                else:
                    sheet.merge_range(row, 5, row+a, 5,
                                      line_in[i].name, format_data)
                row = row + a + 1
                local_max = len(line_in[i].name)
                if local_max > max_len[i]:
                    max_len[i] = local_max

            row = row_real
            line_in = partners.process_line_out_ids if partners.process_line_out_ids else [
                '-']
            for i, el in enumerate(difference(len_out)):
                a = el - 1
                clients = ', '.join([x.name for x in line_in[i].output_id])
                ouputs = ', '.join([x.name for x in line_in[i].client_id])
                if a == 0:
                    sheet.write(
                        row, 6, clients, format_data)
                    sheet.write(
                        row, 7, ouputs, format_data)
                else:
                    sheet.merge_range(
                        row, 6, row+a, 6, clients, format_data)
                    sheet.merge_range(
                        row, 7, row+a, 7, ouputs, format_data)
                row = row + a + 1
                local_max = max(len(clients), len(ouputs))
                if local_max > max_len[i]:
                    max_len[i] = local_max

            init = row_real
            for h in max_len:
                print(h)
                if h > 24:
                    sheet.set_row(init, h/2)
                if h == 24:
                    sheet.set_row(init, h)
                init += 1

            sheet.merge_range(row, 0, row, 7, 'RECURSOS', format_header)
            row += 1
            sheet.merge_range(row, 0, row, 1, 'TIPO', format_header)
            sheet.merge_range(row, 2, row, 5, 'NOMBRE', format_header)
            sheet.merge_range(row, 6, row, 7, 'DESCRIPCIÓN', format_header)
            row += 1

            for resource in partners.resource_ids:
                sheet.merge_range(
                    row, 0, row, 1, resource.type_id.name if resource.type_id else '', format_data)
                sheet.merge_range(row, 2, row, 5, resource.name, format_data)
                sheet.merge_range(
                    row, 6, row, 7, resource.description, format_data)
                row += 1

            sheet.merge_range(row, 0, row, 1, 'ELABORADO POR', format_header)
            sheet.merge_range(row, 2, row, 5, 'REVISADO POR', format_header)
            sheet.merge_range(row, 6, row, 7, 'VALIDADO POR', format_header)
            row += 1

            el = '\n'.join([x.user_id.name for x in partners.elaboration_step])
            re = '\n'.join([x.user_id.name for x in partners.review_step])
            va = '\n'.join([x.user_id.name for x in partners.validation_step])
            sheet.merge_range(row, 0, row, 1, el, format_data)
            sheet.merge_range(row, 2, row, 5, re, format_data)
            sheet.merge_range(row, 6, row, 7, va, format_data)
            row += 1
            date_elaborate = partners.date_elaborate.strftime(
                '%d/%m/%Y') if partners.date_elaborate else '-'
            date_review = partners.date_review.strftime(
                '%d/%m/%Y') if partners.date_review else '-'
            date_validate = partners.date_validate.strftime(
                '%d/%m/%Y') if partners.date_validate else '-'
            sheet.merge_range(row, 0, row, 1, date_elaborate, format_data)
            sheet.merge_range(row, 2, row, 5, date_review, format_data)
            sheet.merge_range(row, 6, row, 7, date_validate, format_data)

        workbook.close()
