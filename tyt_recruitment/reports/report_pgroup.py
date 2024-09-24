from odoo import api, fields, models
from datetime import datetime
from odoo.modules.module import get_module_resource
from io import BytesIO
import xlsxwriter

class ReportCustomerProspectGroupXlsx(models.AbstractModel):
    _name = 'report.tyt_recruitment.report_pgroup'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet('Reporte de requisición')
        
        # Column headers
        title_format = workbook.add_format({
            'font_size': 22,
            'font_name': 'Calibri',
            'bg_color': '#31869B', 
            'align': 'center', 
            'valign': 'vcenter', 
            'bold': True, 
            'text_wrap': True, 
            'border': True
        })
        subtitle_format = workbook.add_format({
            'font_size': 16,
            'font_name': 'Calibri',
            'bg_color': '#215967', 
            'align': 'center', 
            'valign': 'vcenter', 
            'text_wrap': True, 
            'border': True
        })
        subtitle_format2 = workbook.add_format({
            'font_size': 11,
            'font_name': 'Calibri',
            'bg_color': '#B7DEE8', 
            'align': 'center', 
            'valign': 'vcenter',
            'bold': True, 
            'text_wrap': True, 
            'border': True
        })
        data_format = workbook.add_format({
            'font_size': 11, 
            'font_name': 'Calibri',
            'align': 'center', 
            'valign': 'vcenter', 
            'text_wrap': True, 
            'border': True
        })
        data_format2 = workbook.add_format({
            'font_size': 11, 
            'font_name': 'Calibri',
            'font_color': '#1F3864',
            'align': 'center', 
            'valign': 'vcenter', 
            'text_wrap': True, 
            'border': True
        })        

        sheet.set_column('A:A', 10)

        sheet.set_column('B:K', 20)

        # Obtener la ruta absoluta de la imagen
        sheet.insert_image('B5', get_module_resource('tyt_recruitment', 'static/src/img', 'logo.png'))

        # Headers rows
        sheet.merge_range('C2:O3', 'LISTA DE PROSPECTOS', title_format)

        sheet.write(4, 2, 'Sitio:', data_format2)
        sheet.write(5, 2, 'Semana:', data_format2)
        sheet.write(6, 2, 'Prospectos:', data_format2)
        sheet.write(7, 2, 'T/M:', data_format2)
        sheet.write(8, 2, 'T/V:', data_format2)
        sheet.write(5, 2, 'Grupo:', data_format2)
        # 'num_format': 'yyyy-mm-dd'
        
        sheet.merge_range('B11:K11', 'DATOS DEL EMPLEADO', subtitle_format)

        sheet.write(11, 1, 'APELLIDO PATERNO', subtitle_format2)
        sheet.write(11, 2, 'APELLIDO MATERNO', subtitle_format2)
        sheet.write(11, 3, 'NOMBRE (S)', subtitle_format2)
        sheet.write(11, 4, 'Número de empleado', subtitle_format2)
        sheet.write(11, 5, 'TELÉFONO', subtitle_format2)
        sheet.write(11, 6, 'FECHA DE NACIMIENTO', subtitle_format2)
        sheet.write(11, 7, 'LUGAR DE NACIMIENTO', subtitle_format2)
        sheet.write(11, 8, 'RFC', subtitle_format2)
        sheet.write(11, 9, 'CURP', subtitle_format2)
        sheet.write(11, 10, 'NSS', subtitle_format2)

        # Data rows
        row = 12
        for partner in partners:

            sheet.write(4, 3, partner.site_id or '', data_format)
            sheet.write(5, 3, partner.week or '', data_format)
            sheet.write(6, 3, partner.prospects or '', data_format)
            sheet.write(7, 3, partner.turn_m or '', data_format)
            sheet.write(8, 3, partner.turn_v or '', data_format)
            sheet.write(5, 6, partner.group or '', data_format)

            for prospect in partner.prospect_ids:
                sheet.write(row, 1, prospect.paternal_surname or '', data_format)
                sheet.write(row, 2, prospect.maternal_surname or '', data_format)
                sheet.write(row, 3, prospect.names or '', data_format)
                sheet.write(row, 4, prospect.employee_number or '', data_format)
                sheet.write(row, 5, prospect.phone_number or '', data_format)
                sheet.write(row, 6, str(prospect.birthday) or '', data_format)
                sheet.write(row, 7, prospect.place_birth or '', data_format)
                sheet.write(row, 8, prospect.rfc or '', data_format)
                sheet.write(row, 9, prospect.curp or '', data_format)
                sheet.write(row, 10, prospect.nss or '', data_format)
                row += 1