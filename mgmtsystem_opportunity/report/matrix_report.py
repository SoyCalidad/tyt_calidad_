# -*- coding: utf-8 -*-
import base64
import io
from datetime import date, datetime
from math import ceil

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from PIL import Image


class WizardMatrix(models.TransientModel):
    _name = "wizard.matrix.report"
    _description = "Reporte de matriz de riesgos y oportunidades"

    company_id = fields.Many2one(
        string=u'Compañia',
        comodel_name='res.company', required=True,

        default=lambda self: self.env.user.company_id.id,
    )

    type = fields.Selection(
        string='Tipo',
        selection=[
            ('risk', 'Riesgo'),
            ('opportunity', 'Oportunidad')],
    )

    matrix_ids = fields.Many2one(
        string='Matriz',
        comodel_name='matrix.matrix',
        relation='matrix_wizard_report_rel',
        column1='matrix_id',
        column2='wizard_id',
    )

    @api.onchange('type')
    def _onchange_type(self):
        return {
            'domain': {
                'matrix_ids': [('type', '=', self.type)]
            }
        }

    def export_xls(self):
        return self.env.ref('mgmtsystem_opportunity.matrix_individual_xlsx').report_action(self.matrix_ids)


class IndividualReport(models.AbstractModel):
    _name = 'report.mgmtsystem_opprisk.report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, matrixes):
        try:
            for matrix in matrixes:
                sheet = workbook.add_worksheet(str(matrix.name))

                format21_c_bold = workbook.add_format(
                    {'font_size': 10, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
                format21_left = workbook.add_format(
                    {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
                format21_gray = workbook.add_format(
                    {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
                format21_red = workbook.add_format(
                    {'font_size': 10, 'bg_color': '#FF0000', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
                format21_gray_bold = workbook.add_format(
                    {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, })
                format21_red_bold = workbook.add_format(
                    {'font_size': 10, 'bg_color': 'red', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, })
                format26_c_bold = workbook.add_format(
                    {'font_size': 26, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})

                format26_c_bold.set_border()
                format21_c_bold.set_border()
                format21_left.set_border()
                format21_gray.set_border()
                format21_gray_bold.set_border()

                prod_row = 4
                i = 0

                sheet.set_column(0, 0, 5)  # nro
                sheet.set_column(1, 1, 16)  # fuente
                sheet.set_column(2, 2, 16)
                sheet.set_column(2, 2, 16)
                sheet.set_column(3, 5, 25)
                sheet.set_column(6, 9, 12)
                sheet.set_column(10, 11, 25)
                sheet.set_column(12, 13, 17)

                sheet.merge_range(prod_row-1, i, prod_row,
                                  i, 'Nro', format21_c_bold)
                i += 1
                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Proceso', format21_c_bold)
                i += 1
                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Área responsable', format21_c_bold)

                sheet.merge_range(
                    'A1:C3', self.env.company.name, format21_c_bold)

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

                i += 1

                sheet.write(prod_row, i, 'Identificado', format21_gray_bold)
                i += 1
                sheet.write(prod_row, i, 'Efecto', format21_gray_bold)
                i += 1
                sheet.write(prod_row, i, 'Causa', format21_gray_bold)
                i += 1
                sheet.merge_range(prod_row-1, i-3, prod_row-1, i-1,
                                  'Modo de fallo/oportunidad potencial', format21_c_bold)
                sheet.merge_range(prod_row-1, i, prod_row-1, i+2,
                                  'Evaluación', format21_c_bold)

                count_cri = 0
                if matrix.line_ids:
                    if matrix.line_ids[0].evaluation_id:
                        for criterio in matrix.line_ids[0].evaluation_id.criterio_ids:
                            count_cri += 1
                            sheet.write(prod_row, i, criterio.name,
                                        format21_gray_bold)
                            i += 1
                sheet.write(prod_row, i, 'Resultado', format21_gray_bold)
                i += 1
                sheet.merge_range(prod_row-1, i-count_cri-1,
                                  prod_row-1, i-1, 'Valoración', format21_c_bold)

                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Acciones abordadas', format21_c_bold)
                var_type = "Riesgo" if matrix.type == "risk" else "Oportunidad"
                var_type += ' ' + matrix.system_id.name if matrix.system_id else ''
                sheet.merge_range(prod_row-4, i-count_cri-4, prod_row-2,
                                  i, 'Matriz de ' + var_type, format26_c_bold)
                i += 1

                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Responsable', format21_c_bold)
                i += 1
                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Fecha de inicio', format21_c_bold)
                i += 1

                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Fecha de cierre', format21_c_bold)
                sheet.merge_range(prod_row-4, i-2, prod_row-4,
                                  i, 'Código: '+str(matrix.code), format21_c_bold)
                sheet.merge_range(prod_row-3, i-2, prod_row-3, i,
                                  'Edición: '+str(matrix.numero), format21_c_bold)
                sheet.merge_range(prod_row-2, i-2, prod_row-2, i, 'Fecha de aprobación: '+str(
                    matrix.date_validate or "Sin definir"), format21_c_bold)
                i += 1

                prod_row += 1
                count = 1

                lines_order = self.env['matrix.block.line'].search(
                    [('id', 'in', matrix.line_ids.ids)], order="block_id")

                block_name = ""
                row_count = 1
                row_a = 0
                line_actual = 0
                last_line = len(lines_order)
                max_height = 20

                for line in lines_order:
                    line_actual += 1
                    i = 0

                    if block_name == "":
                        block_name = line.block_id.name or ""
                        row_a = prod_row
                    else:
                        row_count += 1

                    sheet.write(prod_row, i, count, format21_left)
                    i += 1

                    sheet.write(prod_row, i,
                                line.process_id.name, format21_left)

                    i += 1

                    sheet.write(
                        prod_row, i, line.department_id.name, format21_left)
                    i += 1
                    sheet.write(prod_row, i, line.name, format21_left)
                    i += 1
                    sheet.write(prod_row, i, line.effect, format21_left)
                    i += 1
                    sheet.write(prod_row, i, line.cause, format21_left)
                    i += 1

                    len_action_ids = len(
                        '\n'.join([x.name for x in line.action_ids]))
                    len_name = len(line.name)
                    len_effect = len(line.effect) if line.effect else 0
                    len_cause = len(line.cause) if line.cause else 0

                    max_height = max(len_action_ids, len_name,
                                     len_effect, len_cause)

                    if max_height > 25:
                        max_height = ceil(max_height/25)*10
                    else:
                        max_height = 20

                    sheet.set_row(prod_row, max_height)

                    for result in line.result_ids:
                        if result.value <= 5:
                            sheet.write(prod_row, i, result.value,
                                        format21_red_bold)
                        sheet.write(prod_row, i, result.value, format21_left)
                        i += 1
                    ntr = line.ntr or 0
                    if int(ntr) > 100:
                        sheet.write(prod_row, i, line.ntr, format21_red)
                    else:
                        sheet.write(prod_row, i, line.ntr, format21_gray)
                    i += 1

                    sheet.write(prod_row, i, '\n '.join(
                        x.name for x in line.action_ids), format21_left)
                    i += 1
                    sheet.write(prod_row, i, '\n '.join(
                        x.user_id.name for x in line.action_ids), format21_left)
                    i += 1
                    sheet.write(prod_row, i, '\n '.join(
                        str(x.date_open) for x in line.action_ids), format21_left)
                    i += 1
                    date_deadline = '\n '.join(x.date_deadline.strftime(
                        '%d/%m/%Y') if x.date_deadline else '' for x in line.action_ids)
                    sheet.write(prod_row, i, date_deadline, format21_left)
                    i += 1

                    prod_row += 1
                    count += 1
        except Exception as e:
            print(e)
            raise UserError("Hubo un error al generar el reporte")


class MatrixReportXls(models.AbstractModel):
    _name = 'report.matrix_report_xls.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        try:
            for matrix in lines.matrix_ids:
                sheet = workbook.add_worksheet(str(matrix.name))

                format21_c_bold = workbook.add_format(
                    {'font_size': 10, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
                format21_left = workbook.add_format(
                    {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
                format21_gray = workbook.add_format(
                    {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
                format21_red = workbook.add_format(
                    {'font_size': 10, 'bg_color': '#FF0000', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
                format21_gray_bold = workbook.add_format(
                    {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, })
                format21_red_bold = workbook.add_format(
                    {'font_size': 10, 'bg_color': 'red', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, })
                format26_c_bold = workbook.add_format(
                    {'font_size': 26, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})

                format26_c_bold.set_border()
                format21_c_bold.set_border()
                format21_left.set_border()
                format21_gray.set_border()
                format21_gray_bold.set_border()

                prod_row = 4
                i = 0

                sheet.set_column(0, 0, 5)  # nro
                sheet.set_column(1, 1, 16)  # fuente
                sheet.set_column(2, 2, 16)
                sheet.set_column(2, 2, 16)
                sheet.set_column(3, 5, 25)
                sheet.set_column(6, 9, 12)
                sheet.set_column(10, 11, 25)
                sheet.set_column(12, 13, 17)

                sheet.merge_range(prod_row-1, i, prod_row,
                                  i, 'Nro', format21_c_bold)
                i += 1
                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Proceso', format21_c_bold)
                i += 1
                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Área responsable', format21_c_bold)

                sheet.merge_range(
                    'A1:C3', lines.company_id.name, format21_c_bold)

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

                i += 1

                sheet.write(prod_row, i, 'Identificado', format21_gray_bold)
                i += 1
                sheet.write(prod_row, i, 'Efecto', format21_gray_bold)
                i += 1
                sheet.write(prod_row, i, 'Causa', format21_gray_bold)
                i += 1
                sheet.merge_range(prod_row-1, i-3, prod_row-1, i-1,
                                  'Modo de fallo/oportunidad potencial', format21_c_bold)
                sheet.merge_range(prod_row-1, i, prod_row-1, i+2,
                                  'Evaluación', format21_c_bold)

                count_cri = 0
                if matrix.line_ids:
                    if matrix.line_ids[0].evaluation_id:
                        for criterio in matrix.line_ids[0].evaluation_id.criterio_ids:
                            count_cri += 1
                            sheet.write(prod_row, i, criterio.name,
                                        format21_gray_bold)
                            i += 1
                sheet.write(prod_row, i, 'Resultado', format21_gray_bold)
                i += 1
                sheet.merge_range(prod_row-1, i-count_cri-1,
                                  prod_row-1, i-1, 'Valoración', format21_c_bold)

                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Acciones abordadas', format21_c_bold)
                var_type = "Riesgo" if matrix.type == "risk" else "Oportunidad"
                sheet.merge_range(prod_row-4, i-count_cri-4, prod_row-2,
                                  i, 'Matriz de '+var_type, format26_c_bold)
                i += 1

                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Responsable', format21_c_bold)
                i += 1
                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Fecha de inicio', format21_c_bold)
                i += 1

                sheet.merge_range(prod_row-1, i, prod_row, i,
                                  'Fecha de cierre', format21_c_bold)
                sheet.merge_range(prod_row-4, i-2, prod_row-4,
                                  i, 'Código: '+str(matrix.code), format21_c_bold)
                sheet.merge_range(prod_row-3, i-2, prod_row-3, i,
                                  'Edición: '+str(matrix.numero), format21_c_bold)
                sheet.merge_range(prod_row-2, i-2, prod_row-2, i, 'Fecha de aprobación: '+str(
                    matrix.date_validate or "Sin definir"), format21_c_bold)
                i += 1

                prod_row += 1
                count = 1

                lines_order = self.env['matrix.block.line'].search(
                    [('id', 'in', matrix.line_ids.ids)], order="block_id")

                block_name = ""
                row_count = 1
                row_a = 0
                line_actual = 0
                last_line = len(lines_order)

                max_height = 20

                for line in lines_order:
                    line_actual += 1
                    i = 0

                    if block_name == "":
                        block_name = line.block_id.name or ""
                        row_a = prod_row
                    else:
                        row_count += 1

                    sheet.write(prod_row, i, count, format21_left)
                    i += 1

                    sheet.write(prod_row, i, line.process_id.name,
                                format21_left)

                    i += 1

                    sheet.write(
                        prod_row, i, line.department_id.name, format21_left)
                    i += 1
                    sheet.write(prod_row, i, line.name, format21_left)
                    i += 1
                    sheet.write(prod_row, i, line.effect, format21_left)
                    i += 1
                    sheet.write(prod_row, i, line.cause, format21_left)
                    i += 1

                    len_action_ids = len(
                        '\n'.join([x.name for x in line.action_ids]))
                    len_name = len(line.name)
                    len_effect = len(line.effect) if line.effect else 0
                    len_cause = len(line.cause) if line.cause else 0

                    max_height = max(len_action_ids, len_name,
                                     len_effect, len_cause)

                    if max_height > 25:
                        max_height = ceil(max_height/25)*10

                    sheet.set_row(prod_row, max_height)

                    for result in line.result_ids:
                        if result.value <= 5:
                            sheet.write(prod_row, i, result.value,
                                        format21_red_bold)
                        sheet.write(prod_row, i, result.value, format21_left)
                        i += 1
                    ntr = line.ntr or 0
                    if int(ntr) > 100:
                        sheet.write(prod_row, i, line.ntr, format21_red)
                    else:
                        sheet.write(prod_row, i, line.ntr, format21_gray)
                    i += 1

                    sheet.write(prod_row, i, '\n '.join(
                        x.name for x in line.action_ids), format21_left)
                    i += 1
                    sheet.write(prod_row, i, '\n '.join(
                        x.user_id.name for x in line.action_ids), format21_left)
                    i += 1
                    sheet.write(prod_row, i, '\n '.join(
                        str(x.date_open) for x in line.action_ids), format21_left)
                    i += 1
                    date_deadline = '\n '.join(x.date_deadline.strftime(
                        '%d/%m/%Y') if x.date_deadline else '' for x in line.action_ids)
                    sheet.write(prod_row, i, date_deadline, format21_left)
                    i += 1

                    prod_row += 1
                    count += 1
        except Exception as e:
            print(e)
            raise UserError("Hubo un error al generar el reporte")
