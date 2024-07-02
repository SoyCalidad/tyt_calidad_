# -*- coding: utf-8 -*-
import base64
import datetime
import io

from PIL import Image

from odoo import api, fields, models
from odoo.exceptions import ValidationError, Warning


class MaintananceRequestWizard(models.TransientModel):
    _name = 'maintenance.request.wizard'

    maintenance_request_id = fields.Many2one(
        'maintenance.request', string='Petición de mantenimiento', required=True, domain="[('type_line','=','maintenance')]")

    def action_print(self):
        id = self.maintenance_request_id.id
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'is_wizard': True,
            'id': id,
        }
        return self.env.ref('mgmtsystem_infrastructure.action_report_request').report_action(self, data=datas)
    
class CalibrationRequestWizard(models.TransientModel):
    _name = 'calibration.request.wizard'

    calibration_request_id = fields.Many2one(
        'maintenance.request', string='Petición de mantenimiento', required=True, domain="[('type_line','=','calibration')]")

    def action_print(self):
        id = self.calibration_request_id.id
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'is_wizard': True,
            'id': id,
        }
        return self.env.ref('mgmtsystem_infrastructure.action_report_request').report_action(self, data=datas)


class ReportRequestReport(models.AbstractModel):
    _name = 'report.mgmtsystem_infrastructure.report_request'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, maintenance_plan_id):
        try:

            format_1 = workbook.add_format(
                {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
            format_header = workbook.add_format(
                {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True})

            format_1.set_border()
            format_header.set_border()

            sheet = workbook.add_worksheet('Registro de mantenimiento')

            if data and data.get('is_wizard'):
                maintenance_plan_id = self.env['maintenance.request'].browse(
                    data['id'])

            sheet.merge_range(0, 0, 1, 0, '', format_1)
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
            sheet.insert_image('A1:A2', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
            sheet.merge_range(
                'A1:A2', self.env.user.company_id.name or "company", format_header)
            sheet.merge_range(
                0, 1, 1, 3, maintenance_plan_id.name, format_header)
            sheet.merge_range(0, 4, 0, 5, 'CÓDIGO: APY-MAN-1', format_header)
            sheet.merge_range(1, 4, 1, 5, 'FECHA DE IMPRESIÓN: %s' % (
                datetime.datetime.today().strftime('%d/%m/%Y')), format_header)

            sheet.write(3, 0, 'Creado por', format_header)
            sheet.merge_range(
                3, 1, 3, 2, maintenance_plan_id.employee_id.name, format_1)
            sheet.write(3, 3, 'Tipo de mantenimiento', format_header)
            sheet.merge_range(
                3, 4, 3, 5, maintenance_plan_id.maintenance_type, format_1)
            sheet.write(4, 0, 'Nombre de los equipos', format_header)
            # sheet.merge_range(4, 1, 4, 2, ', '.join([x.name for x in maintenance_plan_id.equipment_id]))
            sheet.merge_range(
                4, 1, 4, 2, maintenance_plan_id.equipment_id.name, format_1)
            sheet.write(4, 3, 'Fecha prevista', format_header)
            sheet.merge_range(
                4, 4, 4, 5, maintenance_plan_id.schedule_date, format_1)
            sheet.write(5, 0, 'Encargado de la validación', format_header)
            sheet.merge_range(
                5, 1, 5, 2, maintenance_plan_id.responsable_id.name, format_1)
            sheet.write(5, 3, 'Fecha de ejecución', format_header)
            sheet.merge_range(
                5, 4, 5, 5, maintenance_plan_id.close_date, format_1)
            sheet.write(6, 0, 'Responsable de la ejecución', format_header)
            sheet.merge_range(
                6, 1, 6, 2, maintenance_plan_id.user_id.name, format_1)
            sheet.write(6, 3, 'Linea del mantenimiento', format_header)
            sheet.merge_range(
                6, 4, 6, 5, maintenance_plan_id.maintenance_line_id.name, format_1)
            sheet.write(7, 0, 'Equipo de mantenimiento', format_header)
            sheet.merge_range(
                7, 1, 7, 5, maintenance_plan_id.maintenance_team_id.name, format_1)
            sheet.write(8, 0, 'Costo', format_header)
            sheet.merge_range(8, 1, 8,  5, maintenance_plan_id.cost, format_1)

            sheet.merge_range(
                10, 0, 10, 5, 'Descripción de las actividades', format_header)
            sheet.merge_range(11, 0, 11, 5, maintenance_plan_id.description, format_1)

            sheet.merge_range(13, 1, 13, 2, 'Solicitado por', format_header)
            sheet.write(15, 1, 'Nombre', format_header)
            sheet.write(15, 2, maintenance_plan_id.employee_id.name, format_1)
            sheet.write(16, 1, 'Firma', format_header)
            sheet.write(16, 2, '', format_1)

            sheet.merge_range(13, 4, 13, 5, 'Ejecutado por', format_header)
            sheet.write(15, 4, 'Nombre', format_header)
            sheet.write(
                15, 5, maintenance_plan_id.activity_user_id.name, format_1)
            sheet.write(16, 4, 'Firma', format_header)
            sheet.write(16, 5, '', format_1)

            sheet.set_row(11, 200)
            sheet.set_row(16, 45)
            sheet.set_row(17, 45)
            sheet.set_column(0, 5, 25)

        except Exception as e:
            print(e)
            raise Warning("Hubo un error al generar el reporte")
