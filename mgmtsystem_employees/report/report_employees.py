# -*- coding: utf-8 -*-
import base64
import io
from PIL import Image
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

# Reporte de datos del empleado en formato excel

SEX = {
    'male': 'Hombre',
    'female': 'Mujer',
    'other': 'Otro'
}

MARITAL = {
    'single': 'Soltero(a)',
    'married': 'Casado(a)',
    'cohabitant': 'Cohabitante legal',
    'widower': 'Viudo(a)',
    'divorced': 'Divorciado',
}


class EmployeeDataReport(models.AbstractModel):
    _name = 'report.mgmtsystem_employees.employess_report'
    _inherit = ['report.report_xlsx.abstract', 'mgmtsystem.code']
    _description = 'Datos de empleados'

    def generate_xlsx_report(self, workbook, data, employee):
        try:

            format21_c_bold = workbook.add_format(
                {'font_size': 10, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
            format26_c_bold = workbook.add_format(
                {'font_size': 14, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
            format21_left = workbook.add_format(
                {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
            format21_gray = workbook.add_format(
                {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
            format21_gray_bold = workbook.add_format(
                {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, })
            format21_gray_rotate_bold = workbook.add_format(
                {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, })

            format21_c_bold.set_border()
            format26_c_bold.set_border()
            format21_left.set_border()
            format21_gray.set_border()
            format21_gray_bold.set_border()
            format21_gray_rotate_bold.set_border()
            format21_gray_rotate_bold.set_rotation(90)

            sheet = workbook.add_worksheet('Ficha de datos del empleado')

            sheet.set_column(0, 0, 5)
            sheet.set_column(1, 1, 30)
            sheet.set_column(2, 2, 11)
            sheet.set_column(3, 9, 5)
            sheet.set_column(10, 11, 10)

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
            sheet.merge_range(
                'C1:K3', 'FICHA DE DATOS DEL EMPLEADO', format26_c_bold)
            datetime = fields.Datetime.now(self)
            sheet.merge_range('L1:L3', 'Fecha: ' +
                              str(datetime), format21_c_bold)

            sheet.merge_range(5, 0, 5, 11, 'I. DATOS PERSONALES',
                              format21_c_bold)

            sheet.merge_range(6, 0, 6, 1, 'NOMBRES COMPLETOS', format21_c_bold)
            sheet.merge_range(6, 2, 6, 11, employee.name, format21_left)

            sheet.merge_range(7, 0, 7, 1, 'TIPO DE DOCUMENTO', format21_c_bold)
            sheet.merge_range(7, 2, 7, 11, '', format21_left)

            sheet.merge_range(8, 0, 8, 1, 'N° DE DOCUMENTO', format21_c_bold)
            sheet.merge_range(
                8, 2, 8, 11, employee.identification_id, format21_left)

            sheet.merge_range(9, 0, 9, 1, 'NACIONALIDAD', format21_c_bold)
            sheet.merge_range(
                9, 2, 9, 11, employee.country_id.name, format21_left)

            sheet.merge_range(
                10, 0, 11, 1, 'FECHA DE NACIMIENTO', format21_c_bold)
            sheet.merge_range(10, 2, 11, 11, employee.birthday, format21_left)

            sheet.merge_range(11, 0, 11, 1, 'DIRECCIÓN', format21_c_bold)
            sheet.merge_range(
                11, 2, 11, 11, employee.address_home_id.street, format21_left)

            sheet.merge_range(12, 0, 12, 1, 'SEXO', format21_c_bold)
            sheet.merge_range(
                12, 2, 12, 5, SEX[employee.gender], format21_left)

            sheet.merge_range(12, 6, 12, 8, 'ESTADO CIVIL', format21_c_bold)
            sheet.merge_range(
                12, 9, 12, 11, MARITAL[employee.marital], format21_left)

            sheet.merge_range(
                13, 0, 13, 1, 'CORREO ELECTRÓNICO', format21_c_bold)
            sheet.merge_range(
                13, 2, 13, 11, employee.work_email, format21_left)

            sheet.merge_range(14, 0, 14, 1, 'CELULAR', format21_c_bold)
            sheet.merge_range(
                14, 2, 14, 11, employee.address_home_id.phone, format21_left)

            sheet.merge_range(15, 0, 15, 11, 'II. CARACTERÍSTICAS',
                              format21_c_bold)

            sheet.merge_range(16, 0, 16, 1, 'TIPO DE SANGRE', format21_c_bold)
            sheet.merge_range(
                16, 2, 16, 11, dict(employee._fields['type_blood'].selection).get(employee.type_blood), format21_left)

            sheet.merge_range(
                17, 0, 17, 1, 'LICENCIA DE CONDUCIR', format21_c_bold)
            sheet.merge_range(
                17, 2, 17, 11, employee.license_driver, format21_left)

            sheet.merge_range(18, 0, 18, 1, 'CATEGORÍA', format21_c_bold)
            sheet.merge_range(
                18, 2, 18, 11, dict(employee._fields['category_driver'].selection).get(employee.category_driver), format21_left)

            sheet.merge_range(19, 0, 19, 11, 'III. EDUCACIÓN',
                              format21_c_bold)

            sheet.merge_range(20, 0, 20, 1, 'NIVEL', format21_c_bold)
            sheet.merge_range(20, 2, 20, 11, employee.level, format21_left)

            sheet.merge_range(21, 0, 21, 1, 'INSTITUCIÓN', format21_c_bold)
            sheet.merge_range(
                21, 2, 21, 11, employee.institution, format21_left)

            sheet.merge_range(22, 0, 22, 1, 'PROFESIÓN', format21_c_bold)
            sheet.merge_range(
                22, 2, 22, 11, employee.profession, format21_left)

            sheet.merge_range(23, 0, 23, 11, 'IV. DATOS LABORALES',
                              format21_c_bold)

            sheet.merge_range(
                24, 0, 24, 1, 'UBICACIÓN DEL TRABAJO', format21_c_bold)
            sheet.merge_range(
                24, 2, 24, 11, employee.work_location, format21_left)

            sheet.merge_range(
                25, 0, 25, 1, 'CORREO ELECTRÓNICO DEL TRABAJO', format21_c_bold)
            sheet.merge_range(
                25, 2, 25, 11, employee.work_email, format21_left)

            sheet.merge_range(
                26, 0, 26, 1, 'MÓVIL DEL TRABAJO', format21_c_bold)
            sheet.merge_range(
                26, 2, 26, 11, employee.mobile_phone, format21_left)

            sheet.merge_range(
                27, 0, 27, 1, 'TELÉFONO DEL TRABAJO', format21_c_bold)
            sheet.merge_range(
                27, 2, 27, 11, employee.work_phone, format21_left)

            sheet.merge_range(
                28, 0, 28, 1, 'ÁREA/DEPARTAMENTO', format21_c_bold)
            sheet.merge_range(
                28, 2, 28, 11, employee.department_id.name, format21_left)

            sheet.merge_range(29, 0, 29, 1, 'CARGO/OCUPACIÓN', format21_c_bold)
            sheet.merge_range(
                29, 2, 29, 11, employee.job_id.name, format21_left)

            sheet.merge_range(30, 0, 30, 1, 'RESPONSABLE', format21_c_bold)
            sheet.merge_range(
                30, 2, 30, 11, employee.parent_id.name, format21_left)

            sheet.merge_range(31, 0, 31, 1, 'MONITOR', format21_c_bold)
            sheet.merge_range(
                31, 2, 31, 11, employee.coach_id.name, format21_left)

            sheet.merge_range(
                32, 0, 32, 1, 'HORAS DE TRABAJO', format21_c_bold)
            sheet.merge_range(
                32, 2, 32, 11, employee.resource_calendar_id.name, format21_left)

            sheet.merge_range(33, 0, 33, 1, 'CUENTA BANCARIA', format21_c_bold)
            sheet.merge_range(
                33, 2, 33, 11, employee.bank_account_id.acc_number, format21_left)

            sheet.merge_range(34, 0, 34, 1, 'BANCO', format21_c_bold)
            sheet.merge_range(
                34, 2, 34, 11, employee.bank_account_id.bank_id.name if employee.bank_account_id.bank_id else '', format21_left)

            sheet.merge_range(35, 0, 35, 3, '', format21_left)
            sheet.merge_range(35, 4, 35, 10, '', format21_left)
            sheet.write(35, 11, '', format21_left)

            sheet.merge_range(36, 0, 36, 3, 'RRHH', format21_c_bold)
            sheet.merge_range(
                36, 4, 36, 10, 'FIRMA DEL TRABAJADOR', format21_c_bold)
            sheet.write(36, 11, 'HUELLA DACTILAR', format21_c_bold)

            sheet.set_row(35, 80)
            sheet.set_row(36, 30)

        except Exception as e:
            raise UserError("Hubo un error al generar el reporte")
