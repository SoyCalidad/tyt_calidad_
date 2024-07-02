import base64
import io

from PIL import Image

from odoo import api, fields, models
from odoo.http import request


class infrastructureWizard(models.TransientModel):
    _name = 'mgmtsystem.infrastructure.wizard'

    infrastructure_id = fields.Many2one(
        'mgmtsystem.infrastructure', string='Inventariado', required=True)

    def action_print(self):
        ids = self.infrastructure_id.id
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': ids,
            'is_wizard': True,
        }
        return self.env.ref('mgmtsystem_infrastructure.infrastructure_xlsx').report_action(self, data=datas)


class EquipmentWizard(models.TransientModel):
    _name = 'maintenance.equipment.wizard'

    equipment_ids = fields.Many2many('maintenance.equipment', string='Equipos')

    def action_print(self):
        if not self.equipment_ids:
            equipment_ids = self.env['maintenance.equipment'].search([])
        else:
            equipment_ids = self.equipment_ids
        return self.env.ref('mgmtsystem_infrastructure.equipment_xlsx_report').report_action(equipment_ids)


class EquipmentReport(models.AbstractModel):
    _name = 'report.equipment_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, items):
        format21_c_bold = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'bg_color': '#A0A0A0', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': True})
        format21_left_bold = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'bg_color': '#EEEEEE', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': True})
        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'left', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': True})

        if data.get('is_wizard'):
            items = self.env['mgmtsystem.infrastructure'].browse(data['ids'])

        sheet = workbook.add_worksheet('Equipos')

        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 3, 24)
        sheet.set_column(4, 4, 18)
        sheet.set_column(5, 5, 27)
        sheet.set_column(6, 6, 18)
        sheet.set_column(7, 7, 45)

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
        sheet.insert_image('A1:A3', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})

        sheet.merge_range(
            'A1:B3', self.env.user.company_id.name or "", format21_c_bold)
        sheet.merge_range(
            'C1:G3', 'EQUIPOS', format21_c_bold)
        sheet.write(
            'H1', 'Código: ', format21_c_bold)
        sheet.merge_range(
            'H2:H3', 'Fecha de impresión:\n %s' % str(fields.Datetime.now()), format21_c_bold)

        sheet.write('A4', 'Item', format21_left_bold)
        sheet.write('B4', 'Nombre del equipo', format21_left_bold)
        sheet.write('C4', 'Ref.Interna', format21_left_bold)
        sheet.write('D4', 'Categoría', format21_left_bold)
        sheet.write('E4', 'F.Adquisición', format21_left_bold)
        sheet.write('F4', 'Ubicación', format21_left_bold)
        sheet.write('G4', 'Fecha de desecho', format21_left_bold)
        sheet.write('H4', 'Descripción', format21_left_bold)

        row = 4
        count = 0

        for equipment in items:
            column = 0
            count += 1
            sheet.write(row, column, count, format21_left)
            column += 1
            sheet.write(row, column, equipment.name, format21_left)
            column += 1
            sheet.write(
                row, column, equipment.default_code, format21_left)
            column += 1
            sheet.write(
                row, column, equipment.category_id.name, format21_left)
            column += 1
            sheet.write(
                row, column, equipment.assign_date.strftime('%d/%m/%Y') if equipment.assign_date else '', format21_left)
            column += 1
            sheet.write(
                row, column, equipment.location or "", format21_left)
            column += 1
            sheet.write(
                row, column, equipment.scrap_date.strftime('%d/%m/%Y') if equipment.scrap_date else '', format21_left)
            column += 1
            sheet.write(row, column, equipment.note or "",
                        format21_left)
            row += 1


class InfrastructureReport(models.AbstractModel):
    _name = 'report.mgmtsystem_infrastructure_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, items):
        format21_c_bold = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'bg_color': '#A0A0A0', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': True})
        format21_left_bold = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'bg_color': '#EEEEEE', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': True})
        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'left', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': True})

        if data.get('is_wizard'):
            items = self.env['mgmtsystem.infrastructure'].browse(data['ids'])

        for item in items:
            sheet = workbook.add_worksheet(str(item.name))

            sheet.set_column(0, 0, 5)
            sheet.set_column(1, 1, 30)
            sheet.set_column(2, 3, 24)
            sheet.set_column(4, 4, 18)
            sheet.set_column(5, 5, 27)
            sheet.set_column(6, 6, 18)
            sheet.set_column(7, 7, 45)

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
            sheet.insert_image('A1:A3', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})

            sheet.merge_range(
                'A1:B3', self.env.user.company_id.name or "", format21_c_bold)
            sheet.merge_range(
                'C1:F3', 'FICHERO DE INVENTARIO', format21_c_bold)
            sheet.merge_range(
                'G1:H1', item.edition_id.code or "Sin código", format21_c_bold)
            sheet.merge_range('G2:H2', item.numero, format21_c_bold)
            sheet.merge_range('G3:H3', 'Fecha: %s' %
                              (item.date_elaborate), format21_c_bold)

            sheet.write('A4', 'Item', format21_left_bold)
            sheet.write('B4', 'Nombre del equipo', format21_left_bold)
            sheet.write('C4', 'Ref.Interna', format21_left_bold)
            sheet.write('D4', 'Categoría', format21_left_bold)
            sheet.write('E4', 'F.Adquisición', format21_left_bold)
            sheet.write('F4', 'Ubicación', format21_left_bold)
            sheet.write('G4', 'Fecha de desecho', format21_left_bold)
            sheet.write('H4', 'Descripción', format21_left_bold)

            row = 4
            count = 0

            if item.lines_ids:
                for line in item.lines_ids:
                    column = 0
                    count += 1
                    sheet.write(row, column, count, format21_left)
                    column += 1
                    sheet.write(row, column, line.name, format21_left)
                    column += 1
                    sheet.write(
                        row, column, line.equipment_id.default_code, format21_left)
                    column += 1
                    sheet.write(
                        row, column, line.category_id.name or "", format21_left)
                    column += 1
                    sheet.write(
                        row, column, line.equipment_id.assign_date.strftime('%d/%m/%Y') if line.equipment_id.assign_date else '', format21_left)
                    column += 1
                    sheet.write(row, column, line.location or "",
                                format21_left)
                    column += 1
                    sheet.write(row, column, line.scrap_date.strftime('%d/%m/%Y') if line.scrap_date else '',
                                format21_left)
                    column += 1
                    sheet.write(
                        row, column, line.equipment_id.note or "", format21_left)
                    row += 1
            else:
                for equipment in item.equipment_ids:
                    column = 0
                    count += 1
                    sheet.write(row, column, count, format21_left)
                    column += 1
                    sheet.write(row, column, equipment.name, format21_left)
                    column += 1
                    sheet.write(
                        row, column, equipment.default_code, format21_left)
                    column += 1
                    sheet.write(
                        row, column, equipment.category_id.name, format21_left)
                    column += 1
                    sheet.write(
                        row, column, equipment.assign_date.strftime('%d/%m/%Y') if equipment.assign_date else '', format21_left)
                    column += 1
                    sheet.write(
                        row, column, equipment.location or "", format21_left)
                    column += 1
                    sheet.write(
                        row, column, equipment.scrap_date.strftime('%d/%m/%Y') if equipment.scrap_date else '', format21_left)
                    column += 1
                    sheet.write(row, column, equipment.note or "",
                                format21_left)
                    row += 1
            row += 1
            elaborates = ", ".join(x.name for x in item.elaborate_ids)
            sheet.write(row, 1, "Elaborado por:", format21_left_bold)
            sheet.write(row+1, 1, elaborates, format21_left)
            sheet.write(row+2, 1, "Fecha: %s" %
                        (item.date_elaborate or ""), format21_left)

            reviews = ", ".join(x.name for x in item.review_ids)
            sheet.write(row, 3, "Revisado por:", format21_left_bold)
            sheet.write(row+1, 3, reviews, format21_left)
            sheet.write(row+2, 3, "Fecha: %s" %
                        (item.date_elaborate or ""), format21_left)

            validates = ", ".join(x.name for x in item.validate_ids)
            sheet.write(row, 5, "Validado por:", format21_left_bold)
            sheet.write(row+1, 5, validates, format21_left)
            sheet.write(row+2, 5, "Fecha: %s" %
                        (item.date_elaborate or ""), format21_left)
