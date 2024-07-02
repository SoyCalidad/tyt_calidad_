# -*- coding: utf-8 -*-
import base64
import io
from collections import defaultdict
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from PIL import Image


class MgmtsystemChangeRequestReportWizard(models.TransientModel):
    _name = 'mgmtsystem.change_request.report_wizard'
    _inherit = 'mgmtsystem.report_wizard'
    _description = 'Mgmtsystem Change Request Report Wizard'

    change_request_ids = fields.Many2many(
        'soycalidad.change_request', string='Planificaciones de cambios', relation='ch_re_report_rel')

    def action_print(self):
        return self.action_print_parameters(
            'soycalidad_improve.action_report_change_request', self.change_request_ids)


class ChangeRequestReportXls(models.AbstractModel):
    _name = 'report.report_change_request'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, matrixes):

        try:
            for i, matrix in enumerate(matrixes, 1):
                sheet = workbook.add_worksheet(
                    'Planificación de cambios ({})'.format(i))

                format21_c_bold = workbook.add_format(
                    {'font_size': 8, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
                format21_gray = workbook.add_format(
                    {'font_size': 10, 'bg_color': '#c0c0c0', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True, 'bold': True})
                format26_c_bold = workbook.add_format(
                    {'font_size': 26, 'bg_color': '#c0c0c0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': True})

                sheet.set_column('A:W', 15)

                company_id = self.env.user.company_id

                buf_image = io.BytesIO(base64.b64decode(company_id.logo))
                im = Image.open(buf_image)
                width, height = im.size
                image_width = width
                image_height = height
                cell_width = 50
                cell_height = 50
                cell_column = 8.43/8*11

                x_scale = cell_width/image_width
                y_scale = cell_height/image_height
                sheet.insert_image('A1', "logo.png", {
                    'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 39})
                sheet.merge_range(
                    'B1:E3', 'SOLICITUD DE CAMBIO', format26_c_bold)
                sheet.write('F1:F1', 'Código: ', format21_c_bold)
                sheet.write('F2:F2', 'Versión: ', format21_c_bold)
                sheet.write('F3:F3', 'Fecha de impresión: ' +
                            datetime.today().strftime('%d/%m/%Y'), format21_c_bold)
                sheet.set_row(2, 22)
                request_date = matrix.request_date.strftime(
                    '%d/%m/%Y') if matrix.request_date else ''
                sheet.write(3, 0, 'Fecha de solicitud', format21_gray)
                sheet.merge_range(3, 1, 3, 2, request_date, format21_c_bold)
                sheet.write(3, 3, 'Solicitante', format21_gray)
                sheet.merge_range(
                    3, 4, 3, 5, matrix.employee_id.name, format21_c_bold)

                background = matrix.background or ''
                sheet.merge_range(
                    4, 0, 4, 5, 'Antecedentes del Cambio (¿Por qué se requiere?):', format21_gray)
                sheet.merge_range(5, 0, 5, 5, background, format21_c_bold)

                if len(background) > 133:
                    sheet.set_row(5, len(background)/(cell_column))

                description = matrix.description or ''
                sheet.merge_range(
                    6, 0, 6, 5, 'Descripción del cambio', format21_gray)
                sheet.merge_range(7, 0, 7, 5, description, format21_c_bold)

                if len(description) > 133:
                    sheet.set_row(7, len(description)/(cell_column))

                # benefit = matrix.benefit or ''
                # sheet.merge_range(
                #     8, 0, 8, 5, 'Acción aplicada para asegurar la conformidad del producto/servicio en el Sistema de gestión', format21_gray)
                # sheet.merge_range(9, 0, 9, 5, benefit, format21_c_bold)

                # if len(benefit) > 133:
                #     sheet.set_row(9, len(benefit)/(cell_column))

                consequence = matrix.consequence or ''
                sheet.merge_range(
                    8, 0, 8, 5, 'Posible impacto en la conformidad del producto/servicio en el Sistema de gestión', format21_gray)
                sheet.merge_range(
                    9, 0, 9, 5, consequence, format21_c_bold)
                if len(consequence) > 133:
                    sheet.set_row(9, len(consequence)/(cell_column))

                sheet.merge_range(10, 0, 10, 5, 'Recursos', format21_gray)
                sheet.merge_range(
                    11, 0, 11, 5, ', '.join([x.name for x in matrix.resource_ids]), format21_c_bold)

                sheet.merge_range(
                    12, 0, 12, 5, 'Necesidad de asignación o reasignación de responsibilidades y autoridades', format21_gray)
                sheet.merge_range(
                    13, 0, 13, 5, matrix.needing, format21_c_bold)

                documents = '\n'.join(
                    [x.name for x in matrix.dms_document_ids])
                sheet.merge_range(
                    14, 0, 14, 5, 'Documentos anexos (si existen)', format21_gray)
                sheet.merge_range(15, 0, 15, 5, documents, format21_c_bold)
                if len(documents) > 15:
                    sheet.set_row(15, len(documents))

                sheet.merge_range(
                    16, 0, 16, 5, 'LOS SIGUIENTES ÍTEMS DEBEN SER DILIGENCIADOS POR EL ADMINISTRADOR DEL CAMBIO', format21_gray)
                sheet.merge_range(17, 0, 17, 1, 'Aprobado', format21_gray)
                x = 'Sí' if matrix.approval else 'No'
                sheet.write(17, 2, x, format21_c_bold)
                sheet.merge_range(
                    17, 3, 17, 4, 'Fecha de respuesta', format21_gray)
                sheet.write(17, 5, matrix.response_date, format21_c_bold)

                sheet.merge_range(
                    18, 0, 18, 5, 'Aprobaciones respectivas', format21_gray)
                sheet.merge_range(19, 0, 19, 1, 'Solicitante', format21_gray)
                sheet.merge_range(
                    19, 2, 19, 3, 'Gestor de cambio', format21_gray)
                sheet.merge_range(19, 4, 19, 5, 'Aprobación', format21_gray)
                sheet.merge_range(
                    20, 0, 20, 1, matrix.employee_id.name, format21_c_bold)
                sheet.merge_range(
                    20, 2, 20, 3, matrix.responsible_id.name, format21_c_bold)
                sheet.merge_range(20, 4, 20, 5, '', format21_c_bold)

                sheet.merge_range(21, 0, 21, 5, 'Acciones', format21_gray)
                sheet.merge_range(22, 0, 22, 1, 'Nombre', format21_gray)
                sheet.write(22, 2, 'Fecha/Hora de inicio', format21_gray)
                sheet.write(22, 3, 'Fecha/Hora de finalización', format21_gray)
                sheet.write(22, 4, 'Responsable', format21_gray)
                sheet.write(22, 5, 'Estado', format21_gray)
                sheet.set_row(22, 22)

                for row, act in enumerate(matrix.action_ids, 23):
                    date_open = act.date_open.strftime(
                        '%d/%m/%Y') if act.date_open else ''
                    date_deadline = act.date_deadline.strftime(
                        '%d/%m/%Y') if act.date_deadline else ''
                    sheet.merge_range(
                        row, 0, row, 1, act.name, format21_c_bold)
                    sheet.write(row, 2, date_open, format21_c_bold)
                    sheet.write(row, 3, date_deadline, format21_c_bold)
                    sheet.write(row, 4, act.user_id.name, format21_c_bold)
                    sheet.write(row, 5, dict(act._fields['state'].selection).get(
                        act.state), format21_c_bold)



        except:
            raise UserError('Error al generar el reporte')
