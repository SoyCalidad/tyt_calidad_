# -*- coding: utf-8 -*-
import base64
import io
from collections import defaultdict
from datetime import datetime
from math import ceil

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from PIL import Image


class MgmtsystemImprovePlanMatrixReportWizard(models.TransientModel):
    _name = 'mgmtsystem.improve_plan_matrix.report_wizard'
    _inherit = 'mgmtsystem.report_wizard'
    _description = 'Mgmtsystem Improve Plan Matrix Report Wizard'

    matrix_ids = fields.Many2many(
        'soycalidad.improve_plan.matrix', string='Matrices de planificación de cambios', relation='im_ma_report_rel')

    def action_print(self):
        return self.action_print_parameters(
            'soycalidad_improve.action_report_improve_plan_matrix', self.matrix_ids)


class MatrixReportXls(models.AbstractModel):
    _name = 'report.report_improve_plan_matrix'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, matrixes):
        try:
            for i, matrix in enumerate(matrixes, 1):
                sheet = workbook.add_worksheet(
                    'Matriz de planificación de cambios ({})'.format(i))

                format21_c_bold = workbook.add_format(
                    {'font_size': 8, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
                format21_gray = workbook.add_format(
                    {'font_size': 10, 'bg_color': '#c0c0c0', 'bold': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
                format26_c_bold = workbook.add_format(
                    {'font_size': 26, 'bg_color': '#c0c0c0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': True})

                sheet.set_column('A:W', 15)
                sheet.set_row(3, 35)
                sheet.set_row(4, 35)

                company_id = self.env.user.company_id

                buf_image = io.BytesIO(base64.b64decode(company_id.logo))
                im = Image.open(buf_image)
                width, height = im.size
                image_width = width
                image_height = height
                cell_width = 50
                cell_height = 50

                x_scale = cell_width/image_width
                y_scale = cell_height/image_height
                sheet.insert_image('A1', "logo.png", {
                    'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 39})
                sheet.merge_range(
                    'B1:H3', 'Matriz de planificación de cambios', format26_c_bold)
                code = matrix.code or ''
                sheet.write('I1:I1', 'Código: ' + code, format21_c_bold)
                sheet.write('I2:I2', 'Versión: ' +
                            str(matrix.version), format21_c_bold)
                date_validate = matrix.date_validate.strftime(
                    '%d/%m/%Y') if matrix.date_validate else ''
                sheet.write('I3:I3', 'Fecha de validación: ' +
                            date_validate, format21_c_bold)

                sheet.merge_range(3, 0, 4, 0, 'Fecha', format21_gray)
                sheet.merge_range(3, 1, 4, 2, 'Descripción', format21_gray)
                sheet.merge_range(3, 3, 4, 3, 'Solicitante', format21_gray)
                sheet.merge_range(
                    3, 4, 4, 4, 'Antecedentes del cambio (¿Por qué se requiere?)', format21_gray)
                sheet.merge_range(3, 5, 4, 5, 'Área', format21_gray)
                # sheet.merge_range(
                #     3, 5, 4, 5, 'Acción aplicada para asegurar la conformidad del producto/servicio en el Sistema de gestión', format21_gray)
                sheet.merge_range(
                    3, 6, 4, 6, 'Posible impacto en la conformidad del producto/servicio en el Sistema de gestión', format21_gray)
                sheet.merge_range(3, 7, 4, 7, 'Recursos', format21_gray)
                sheet.merge_range(
                    3, 8, 4, 8, 'Necesidad de asignación o reasignación de responsibilidades y autoridades', format21_gray)
                row = 5
                for plan in matrix.improve_plan_ids:
                    resources = '\n'.join([x.name for x in plan.resource_ids])
                    targets = '\n'.join([x.name for x in plan.target_ids])
                    request_date = plan.request_date.strftime(
                        '%d/%m/%Y') if plan.request_date else ''
                    employee_id = plan.employee_id.name if plan.employee_id else ''
                    change_request_area_id = plan.change_request_area_id.name if plan.change_request_area_id else ''
                    a = len(resources) if resources else 0
                    b = len(targets) if targets else 0
                    c = len(plan.description) if plan.description else 0
                    d = len(plan.employee_id) if plan.employee_id else 0
                    e = len(plan.consequence) if plan.consequence else 0
                    height = max(a, b, c, d, e)
                    
                    sheet.write(row, 0, request_date, format21_c_bold)
                    sheet.merge_range(
                        row, 1, row, 2, plan.description, format21_c_bold)
                    sheet.write(row, 3, employee_id, format21_c_bold)
                    sheet.write(row, 4, plan.background, format21_c_bold)
                    sheet.write(row, 5, change_request_area_id,
                                format21_c_bold)
                    # sheet.write(row, 5, plan.benefit, format21_c_bold)
                    sheet.write(row, 6, plan.consequence, format21_c_bold)
                    sheet.write(row, 7, resources, format21_c_bold)
                    sheet.write(row, 8, plan.needing, format21_c_bold)

                    if height > 15:
                        height = ceil(height/15)*10
                        
                    sheet.set_row(row, height)
                   
                    row += 1

        except:
            raise UserError('Error al generar el reporte')
