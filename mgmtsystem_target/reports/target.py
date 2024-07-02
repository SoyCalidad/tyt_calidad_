# -*- coding: utf-8 -*-
import base64
import io
import os
import time
from datetime import datetime
from PIL import Image

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TargetSourceReport(models.TransientModel):
    _name = 'target.reports'
    _description = 'Target Source Report'

    target_id = fields.Many2one(
        'mgmtsystem.target', string='Objetivo', required=True)

    def action_print(self):
        return self.env.ref('mgmtsystem_target.action_report_target').report_action(self.target_id)

    def action_print_xls(self):
        return self.env.ref('mgmtsystem_target.action_report_xls_target').report_action(self.target_id)


class PorterForcesReportXLS(models.AbstractModel):
    _name = 'report.mgmtsystem_target.target_xls'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Target Report XLSX'

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
            {'font_size': 13, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'align': 'center', 'border': True, 'bg_color': '#3FBBB2'})
        format_data = workbook.add_format(
            {'font_size': 11, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'border': True})

        for i, indicator in enumerate(partners.indicator_ids):
            sheet = workbook.add_worksheet('Indicador%d' % i)
            sheet.set_column('A:H', 18)
            sheet.merge_range('A1:B2', '', format_data)
            buf_image = io.BytesIO(base64.b64decode(partners.company_id.logo))
            im = Image.open(buf_image)
            width, height = im.size
            image_width = width
            image_height = height

            cell_width = 128.0
            cell_height = 40.0

            x_scale = cell_width/image_width
            y_scale = cell_height/image_height
            sheet.insert_image('A1', "any_name.png", {
                               'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
            sheet.merge_range('C1:G2', 'INDICADORES DE GESTIÓN', format_title)
            sheet.write('H1:H1', partners.code, format_data)
            sheet.write('H2:H2', partners.date_validate, format_data)

            sheet.merge_range('A4:D4', 'OBJETIVO', format_title)
            sheet.merge_range('A5:D5', partners.name, format_data)
            sheet.merge_range(
                'E4:H4', 'PROCESO AL QUE PERTENECE', format_title)
            process = ''
            for pro in partners.process_ids:
                process += pro.name + '\n'
            sheet.merge_range('E5:H5', partners.process_id.name, format_data)

            sheet.merge_range('A6:D6', 'INDICADOR', format_title)
            sheet.merge_range('A7:D7', indicator.name, format_data)
            sheet.merge_range('E6:H6', 'FORMULA DEL INDICADOR', format_title)
            sheet.merge_range(
                'E7:H7', indicator.formula, format_data)

            sheet.merge_range('A8:D9', 'GRÁFICO', format_title)
            sheet.merge_range('E8:G8', 'AÑO', format_title)
            sheet.merge_range('H8:H8', '', format_title)

            data_row = 9
            sheet.merge_range('E9:F9', 'MES', format_title)
            sheet.write('G9', 'META', format_title)
            sheet.write('H9', 'RESULTADO', format_title)
            chart1 = workbook.add_chart({'type': 'column'})
            chart1.set_size({'width': 515.54330709, 'height': 230.92913386})

            for each in indicator.history_ids:
                date = each.date.strftime('%d/%m/%Y') if each.date else ''
                sheet.merge_range(data_row, 4, data_row, 5, date, format_data)
                sheet.write(data_row, 6, each.goal_value, format_data)
                sheet.write(data_row, 7, each.real_result, format_data)

                # chart1.add_series({'values': '=Indicador%d!$G$%d:$H$%d' % (i, data_row+1, data_row+1)})
                data_row += 1
            chart1.add_series({'categories': '=Indicador%d!$E$%d:$E$%d' % (i, data_row-len(indicator.history_ids)+1,
                                                                           data_row), 'values': '=Indicador%d!$H$%d:$H$%d' % (i, data_row-len(indicator.history_ids)+1, data_row)})

            sheet.insert_chart('A10',  chart1)
            data_row = 21 if data_row < 21 else data_row

            sheet.merge_range(data_row, 0, data_row, 7,
                              'ACCIONES', format_title)
            data_row += 1
            actions = partners.action_ids + indicator.action_id
            for each in actions:
                sheet.merge_range(data_row, 0, data_row, 7,
                                  each.name, format_data)
                data_row += 1

            sheet.merge_range(data_row, 0, data_row, 3,
                              'RIESGOS', format_title)
            sheet.merge_range(data_row, 4, data_row, 7,
                              'OPORTUNIDADES', format_title)
            data_row += 1
            for each in partners.risk_ids + partners.opp_ids:
                if each.type == 'risk':
                    sheet.merge_range(data_row, 0, data_row,
                                      3, each.name, format_data)
                else:
                    sheet.merge_range(data_row, 4, data_row,
                                      7, each.name, format_data)
                data_row += 1

        workbook.close()
