# -*- coding: utf-8 -*-
import base64
import io
from collections import defaultdict
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from PIL import Image


class leadsResume(models.TransientModel):
    _name = 'crm.lead.crm_resume'
    _description = 'Reporte de ventas'

    user_id = fields.Many2many('res.users', string='Ejecutivo comercial')
    init_date = fields.Datetime(string='De')
    end_date = fields.Datetime(string='A')
    stage_ids = fields.Many2many('crm.stage', string='Etapa')

    def action_print(self):
        names = [x.name for x in self.user_id]
        init_date = self.init_date.strftime('%d/%m/%Y') if self.init_date else ''
        end_date = self.end_date.strftime('%d/%m/%Y') if self.end_date else ''
        datas = {
            'user_id': names,
            'init_date': self.init_date,
            'end_date': self.end_date,
        }
        leads = self.env['crm.lead'].search([('user_id', 'in', self.user_id.ids), (
            'date_open', '>=', self.init_date), ('date_open', '<=', self.end_date), ('stage_id','in',self.stage_ids.ids)])
        return self.env.ref('soycalidad_crm.action_report_crm_resume').report_action(leads, data=datas)


class leadsResumeReport(models.AbstractModel):
    _name = 'report.soycalidad_crm.crm_resume'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, leads):
        try:
            sheet = workbook.add_worksheet(
                'Reporte de ventas')

            format21_c_bold = workbook.add_format(
                {'font_size': 8, 'bg_color': '#c0c0c0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': True})
            format21_gray = workbook.add_format(
                {'font_size': 10, 'bg_color': '#c0c0c0', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
            format21_row = workbook.add_format(
                {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': True})
            format26_c_bold = workbook.add_format(
                {'font_size': 26, 'bg_color': '#c0c0c0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': True})

            company_id = self.env.user.company_id
            print(data)

            buf_image = io.BytesIO(base64.b64decode(company_id.logo))
            im = Image.open(buf_image)
            width, height = im.size
            image_width = width
            image_height = height
            cell_width = 40
            cell_height = 40

            x_scale = cell_width/image_width
            y_scale = cell_height/image_height
            sheet.insert_image('A1', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale, 'x_offset': 10})
            sheet.merge_range(
                'B1:G2', 'GESTIÓN DE OPORTUNIDADES', format26_c_bold)
            sheet.merge_range('H1:K1', 'Código: ', format21_c_bold)
            sheet.merge_range('H2:K2', 'Edición:', format21_c_bold)

            sheet.merge_range(
                2, 0, 2, 2, 'EJECUTIVO COMERCIAL', format21_c_bold)
            try:
                user_ids = '\n'.join(data['user_id'])
                sheet.set_row(2, len(user_ids))
                sheet.merge_range(2, 3, 2, 6, user_ids, format21_row)
            
                sheet.write(2, 7, 'FECHA DE INICIO', format21_c_bold)
                init_date = data['init_date']
                sheet.write(2, 8, init_date, format21_row)

                sheet.write(2, 9, 'FECHA FIN', format21_c_bold)
                end_date = data['end_date']
                sheet.write(2, 10, end_date, format21_row)
            
            except:
                pass


            sheet.write(3, 0, 'N°', format21_c_bold)
            sheet.write(3, 1, '% DE ÉXITOS', format21_c_bold)
            sheet.merge_range(3, 2, 3, 4, 'ESTADO', format21_c_bold)
            sheet.merge_range(3, 5, 3, 10, 'DESCRIPCIÓN', format21_c_bold)

            sheet.write(4, 0, '1', format21_row)
            sheet.write(4, 1, '100%', format21_row)
            sheet.merge_range(4, 2, 4, 4, 'Venta - Ganado', format21_row)
            sheet.merge_range(
                4, 5, 4, 10, 'Cliente con orden de compra o factura', format21_row)

            sheet.write(5, 0, '2', format21_row)
            sheet.write(5, 1, '75%', format21_row)
            sheet.merge_range(
                5, 2, 5, 4, 'Oportunidad (Alta) - Reunión de cierre', format21_row)
            sheet.merge_range(
                5, 5, 5, 10, 'Cliente con documentacion firmada completa', format21_row)

            sheet.write(6, 0, '3', format21_row)
            sheet.write(6, 1, '50%', format21_row)
            sheet.merge_range(
                6, 2, 6, 4, 'Prospecto (Media) -Segunda reunión', format21_row)
            sheet.merge_range(
                6, 5, 6, 10, 'Cliente con mas de una Segunda llamada o reunión y propuestas entregadas y revisadas.', format21_row)

            sheet.write(7, 0, '4', format21_row)
            sheet.write(7, 1, '25%', format21_row)
            sheet.merge_range(
                7, 2, 7, 4, ' Interesado ( Baja)- Primera reunión', format21_row)
            sheet.merge_range(
                7, 5, 7, 10, 'Cliente solicita se le envie informacion (Tiene datos minimos Necesarios: Nombre de Contacto, Teléfono, Mail)', format21_row)

            sheet.write(8, 0, '5', format21_row)
            sheet.write(8, 1, '0%', format21_row)
            sheet.merge_range(8, 2, 8, 4, 'Perdido', format21_row)
            sheet.merge_range(
                8, 5, 8, 10, 'Cliente Desiste de la propuesta y/o Negociación (Motivo descrito en comentario)', format21_row)

            sheet.write(9, 0, '6', format21_row)
            sheet.write(9, 1, '-', format21_row)
            sheet.merge_range(9, 2, 9, 4, 'Primer contacto', format21_row)
            sheet.merge_range(
                9, 5, 9, 10, 'Se llamó por primera vez al contacto, no respondé o aún no sabe de nuestros servicios.', format21_row)

            sheet.write(10, 0, '% DE ÉXITO', format21_c_bold)
            sheet.write(10, 1, 'INGRESO ESTIMADO', format21_c_bold)
            sheet.write(10, 2, 'PRODUCTO/SERVICIO', format21_c_bold)
            sheet.write(10, 3, 'NOTAS INTERNAS', format21_c_bold)
            sheet.write(10, 4, 'ESTADO', format21_c_bold)
            sheet.write(10, 5, 'EJECUTIVO', format21_c_bold)
            sheet.write(10, 6, 'NOMBRE DE LA OPORTUNIDAD', format21_c_bold)
            sheet.write(10, 7, 'TELÉFONO', format21_c_bold)
            sheet.write(10, 8, 'CORREO', format21_c_bold)
            sheet.write(10, 9, 'MEDIO DE CAPTACIÓN', format21_c_bold)
            sheet.write(10, 10, 'CATEGORÍA', format21_c_bold)

            sheet.set_row(3, 20)
            sheet.set_row(10, 22)
            sheet.set_column('A:K', 25)
            current_contact_column = 11

            for i, lead in enumerate(leads, 11):
                current_contact_column = 11
                sheet.write(i, 0, lead.probability, format21_row)
                sheet.write(i, 1, lead.planned_revenue, format21_row)
                sheet.write(i, 2, '', format21_row)
                sheet.write(i, 3, lead.description, format21_row)
                sheet.write(i, 4, lead.stage_id.name, format21_row)
                sheet.write(i, 5, lead.user_id.name, format21_row)
                sheet.write(i, 6, lead.name, format21_row)
                sheet.write(i, 7, lead.partner_address_phone, format21_row)
                sheet.write(i, 8, lead.email_from, format21_row)
                sheet.write(i, 9, lead.medium_id.name, format21_row)
                sheet.write(i, 10, lead.main_tag_id.name, format21_row)
                meeting_data = self.env['calendar.event'].search(
                    [('opportunity_id', '=', lead.id)])
                meeting_data_len = len(meeting_data)

                for meet in meeting_data:
                    sheet.write(10, current_contact_column,
                                'FECHA CONTACTO', format21_c_bold)
                    sheet.write(10, current_contact_column + 1,
                                'COMENTARIO', format21_c_bold)
                    start_datetime = meet.start_datetime.strftime(
                        '%d/%m/%Y') if meet.start_datetime else ''
                    sheet.write(i, current_contact_column,
                                start_datetime, format21_row)
                    sheet.write(i, current_contact_column + 1,
                                meet.description, format21_row)
                    sheet.set_column(current_contact_column, 30)
                    current_contact_column += 2

        except:
            raise UserError("Hubo un error al generar el reporte")
