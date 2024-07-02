# -*- coding: utf-8 -*-
import base64
import io
import math
import os
import re as regex
import time
from datetime import datetime

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from PIL import Image


def cleanhtml(raw_html):
    cleanr = regex.compile('<.*?>')
    cleantext = regex.sub(cleanr, '', raw_html)
    #amplifying function
    cleantext = cleantext.replace('&nbsp;', ' ')
    cleantext = cleantext.replace('&amp;', '&')
    cleantext = cleantext.replace('&lt;', '<')
    cleantext = cleantext.replace('&gt;', '>')
    cleantext = cleantext.replace('&quot;', '"')
    cleantext = cleantext.replace('&#39;', "'")    
    return cleantext


class PorterForcesReportXLS(models.AbstractModel):
    _name = 'report.mgmtsystem_process_integration.process_file_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, process):
        """Generate a xls report with the data

        Arguments:
            workbook {object} -- A object that represents a Excel workbook
            data {dict} -- The data of the report
            process {object} -- A class object
        """

        if data.get('model') and data['model'] == 'mgmt.process_2.report.wizard':
            process = self.env['mgmt.process'].browse(data['id'])

        format_title = workbook.add_format(
            {'font_size': 13, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'align': 'center', 'border': True, 'bg_color': '#EEEEEE'})
        format_data = workbook.add_format(
            {'font_size': 9, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'border': True, 'text_wrap': True})  # 12.2 characters
        format_header = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'border': True, 'text_wrap': True, 'bold': True, 'align': 'center', 'bg_color': '#EEEEEE'})

        sheet = workbook.add_worksheet('Ficha del procedimiento')
        sheet.set_column('A:L', 15)

        company_id = self.env.user.company_id

        buf_image = io.BytesIO(base64.b64decode(company_id.logo))
        im = Image.open(buf_image)
        width, height = im.size
        image_width = width
        image_height = height
        cell_width = 60.0
        cell_height = 60.0

        x_scale = cell_width/image_width
        y_scale = cell_height/image_height
        sheet.insert_image('A1', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 35})
        sheet.merge_range('B1:J3', 'CARACTERIZACIÓN DEL PROCESO', format_title)

        process_code = process.code if process.code else ''

        sheet.merge_range('K1:L1', 'Código: ' + process_code, format_data)

        document = self.env['process.edition'].search([
            ('process_id', '=', process.id),
            ('state', '=', 'validate_ok'),
            ('active', '=', True)
        ], order='numero desc', limit=1)
        version = document[0].version if document else ''
        sheet.merge_range(
            'K2:L2', 'Versión: ' + str(version), format_data)
        sheet.merge_range('K3:L3', 'Fecha: ' +
                          datetime.today().strftime('%d/%m/%Y'), format_data)

        sheet.merge_range('A4:F4', 'NOMBRE DEL PROCESO', format_header)
        sheet.merge_range('G4:L4', 'RESPONSABLE DEL PROCESO', format_header)

        sheet.merge_range('A5:F5', process.name, format_data)
        sheet.merge_range('G5:L5', ', '.join(
            [x.name for x in process.responsible_id]), format_data)

        purpose = cleanhtml(document.purpose) if document else ''
        height_1 = len(purpose)//12.27 + 1

        scope = cleanhtml(document.scope) if document else ''
        height_2 = len(scope)//12.27 + 1
        sheet.merge_range('A6:L6', 'OBJETO', format_header)
        sheet.merge_range('A7:L7', purpose, format_data)
        sheet.set_row(6, height_1)
        sheet.merge_range('A8:L8', 'ALCANCE', format_header)
        sheet.merge_range('A9:L9', scope, format_data)
        sheet.set_row(8, height_2)

        print(height_1, height_2)

        len_in = len(process.process_line_in_ids)
        len_plan = len(process.interaction_plan)
        len_ver = len(process.interaction_verify)
        len_do = len(process.interaction_do)
        len_act = len(process.interaction_act)
        len_out = len(process.process_line_out_ids)
        lens = [len_in, len_plan, len_do, len_ver, len_act, len_out]

        max_ = max(lens)
        diff = []
        for l in lens:
            diff.append(max_-l)

        row_real = 12
        row = row_real

        sheet.merge_range('A10:L10', 'INTERACCIONES', format_header)
        sheet.merge_range('A11:D11', 'ENTRADAS', format_header)
        sheet.merge_range('A12:B12', 'PROVEEDOR', format_header)
        sheet.merge_range('C12:D12', 'ENTRADAS', format_header)
        sheet.merge_range('E11:H11', 'PROCESOS', format_header)
        sheet.write('E12', 'PLANEAR', format_header)
        sheet.write('F12', 'HACER', format_header)
        sheet.write('G12', 'VERIFICAR', format_header)
        sheet.write('H12', 'ACTUAR', format_header)
        sheet.merge_range('I11:L11', 'SALIDAS', format_header)
        sheet.merge_range('I12:J12', 'SALIDAS', format_header)
        sheet.merge_range('K12:L12', 'CLIENTE', format_header)

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
        print (max_len)
        height = 20

        line_in = process.process_line_in_ids if process.process_line_in_ids else [
            '-']
        for i, el in enumerate(difference(len_in)):
            a = el - 1
            suppliers = ', '.join(
                [x.name for x in line_in[i].supplier_id])
            inputs = ', '.join([x.name for x in line_in[i].input_id])

            sheet.merge_range(
                row, 0, row+a, 1, suppliers, format_data)
            sheet.merge_range(
                row, 2, row+a, 3, inputs, format_data)
            row = row + a + 1
            local_max = max(len(suppliers), len(inputs))
            print (i)
            if local_max > max_len[i]:
                max_len[i] = local_max

        row = row_real
        line_in = process.interaction_plan if process.interaction_plan else [
            '-']
        for i, el in enumerate(difference(len_plan)):
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
        line_in = process.interaction_do if process.interaction_do else ['-']
        for i, el in enumerate(difference(len_do)):
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
        line_in = process.interaction_verify if process.interaction_verify else [
            '-']
        for i, el in enumerate(difference(len_ver)):
            a = el - 1
            if a == 0:
                sheet.write(row, 6, line_in[i].name, format_data)
            else:
                sheet.merge_range(row, 6, row+a, 6,
                                  line_in[i].name, format_data)
            row = row + a + 1
            local_max = len(line_in[i].name)
            if local_max > max_len[i]:
                max_len[i] = local_max

        row = row_real
        line_in = process.interaction_act if process.interaction_act else ['-']
        for i, el in enumerate(difference(len_act)):
            a = el - 1
            if a == 0:
                sheet.write(row, 7, line_in[i].name, format_data)
            else:
                sheet.merge_range(row, 7, row+a, 7,
                                  line_in[i].name, format_data)
            row = row + a + 1
            local_max = len(line_in[i].name)
            if local_max > max_len[i]:
                max_len[i] = local_max

        row = row_real
        line_in = process.process_line_out_ids if process.process_line_out_ids else [
            '-']
        for i, el in enumerate(difference(len_out)):
            a = el - 1
            clients = ', '.join([x.name for x in line_in[i].output_id])
            ouputs = ', '.join([x.name for x in line_in[i].client_id])
            sheet.merge_range(
                row, 8, row+a, 9, clients, format_data)
            sheet.merge_range(
                row, 10, row+a, 11, ouputs, format_data)
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

        # row = row + 1

        sheet.merge_range(row, 0, row, 11, 'RECURSOS', format_header)
        row += 1
        sheet.merge_range(row, 0, row, 3, 'TIPO', format_header)
        sheet.merge_range(row, 4, row, 7, 'NOMBRE', format_header)
        sheet.merge_range(row, 8, row, 11, 'DESCRIPCIÓN', format_header)
        row += 1

        for re in process.resource_ids:
            sheet.merge_range(row, 0, row, 3, re.type_id.name if re.type_id else '', format_data)
            sheet.merge_range(
                row, 4, row, 7, re.name, format_data)
            sheet.merge_range(row, 8, row, 11, re.description, format_data)
            row += 1

        sheet.merge_range(
            row, 0, row, 11, 'CRITERIOS Y MÉTODOS DE CONTROL', format_header)
        row += 1
        sheet.merge_range(row, 0, row+1, 1, 'RIESGOS', format_header)
        sheet.merge_range(row, 2, row+1, 3, 'OPORTUNIDADES', format_header)
        sheet.merge_range(row, 4, row, 7, 'OBJETIVOS', format_header)
        sheet.merge_range(row+1, 4, row+1, 5, 'OBJETIVO', format_header)
        sheet.merge_range(row+1, 6, row+1, 7, 'INDICADORES', format_header)
        sheet.merge_range(row, 8, row+1, 11,
                          'REQUISITOS LEGALES', format_header)
        row += 2

        real_row = row

        len_risk = len(process.risk_ids)
        len_opp = len(process.opp_ids)
        len_tar = len(process.target_ids)
        len_leg = len(process.legal_ids)

        line_in = process.risk_ids if process.risk_ids else ['-']
        for i, el in enumerate(difference(len_risk)):
            a = el - 1
            sheet.merge_range(row, 0, row+a, 1, line_in[i].name, format_data)
            row += a + 1

        row = real_row
        line_in = process.opp_ids if process.opp_ids else ['-']
        for i, el in enumerate(difference(len_opp)):
            a = el - 1
            sheet.merge_range(row, 2, row+a, 3, line_in[i].name, format_data)
            row += a + 1

        row = real_row
        line_in = process.target_ids if process.target_ids else ['-']
        for i, el in enumerate(difference(len_tar)):
            a = el - 1
            indicator = '\n'.join([x.name for x in line_in[i].indicator_ids])
            sheet.merge_range(row, 4, row+a, 5, line_in[i].name, format_data)
            sheet.merge_range(row, 6, row+a, 7, indicator, format_data)
            row += a + 1

        row = real_row
        line_in = process.legal_ids if process.legal_ids else ['-']
        for i, el in enumerate(difference(len_leg)):
            a = el - 1
            sheet.merge_range(row, 8, row+a, 11, line_in[i].name, format_data)
            row += a + 1

        sheet.merge_range(row, 0, row, 3, 'ELABORÓ', format_header)
        sheet.merge_range(row, 4, row, 7, 'REVISÓ', format_header)
        sheet.merge_range(row, 8, row, 11, 'APROBÓ', format_header)
        row += 1
        el = '\n'.join([x.user_id.name for x in document.elaboration_step])
        re = '\n'.join([x.user_id.name for x in document.review_step])
        va = '\n'.join([x.user_id.name for x in document.validation_step])
        sheet.merge_range(row, 0, row, 3, el, format_data)
        sheet.merge_range(row, 4, row, 7, re, format_data)
        sheet.merge_range(row, 8, row, 11, va, format_data)

        sheet.set_row(row, 25)

        workbook.close()
