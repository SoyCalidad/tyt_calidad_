from odoo import api, fields, models
from datetime import datetime
from odoo.modules.module import get_module_resource
from io import BytesIO
import xlsxwriter

class ReportCustomerRequisitionXlsx(models.AbstractModel):
    _name = 'report.tyt_recruitment.report_requisition'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):

        if workbook is None:
            output = BytesIO()
            workbook = xlsxwriter.Workbook(output)

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

        sheet.set_column('A:A', 5.14)
        sheet.set_column('B:B', 5.14)
        sheet.set_column('C:C', 5.14)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)
        sheet.set_column('H:H', 10)
        sheet.set_column('I:I', 10)

        # Obtener la ruta absoluta de la imagen
        sheet.insert_image('A1', get_module_resource('tyt_recruitment', 'static/src/img', 'logo.png'))

        # Headers rows
        sheet.merge_range('D2:I3', 'REQUISICIÓN DE PERSONAL', title_format)

        sheet.write(4, 3, 'FECHA DE SOLICITUD:', data_format2)
        sheet.write(5, 3, 'FECHA DE CIERRE:', data_format2)
        sheet.write(6, 3, 'SEMANA:', data_format2)
        # 'num_format': 'yyyy-mm-dd'
        
        sheet.merge_range('D10:I11', 'REQUERIMIENTO', subtitle_format)

        sheet.write(11, 3, 'CAMPAÑA', subtitle_format2)
        sheet.write(11, 4, 'PERSONAL ACTUAL', subtitle_format2)
        sheet.write(11, 5, 'OBJETIVO DE PERSONAL', subtitle_format2)
        sheet.write(11, 6, 'PERSONAL SOLICITADO', subtitle_format2)
        sheet.write(11, 7, 'TURNO', subtitle_format2)
        sheet.write(11, 8, 'PRIORIDAD', subtitle_format2)

        # Data rows
        row = 12
        for partner in partners:

            request_date = str(partner.request_date)
            closing_date = str(partner.closing_date)

            sheet.write(4, 4, request_date or '', data_format)
            sheet.write(5, 4, closing_date or '', data_format)
            sheet.write(6, 4, partner.week or '', data_format)

            for campaign in partner.campaign_ids:
                sheet.write(row, 3, campaign.tag_id.name or '', data_format)
                sheet.write(row, 4, campaign.current_staff or '', data_format)
                sheet.write(row, 5, campaign.goal_staff or '', data_format)
                sheet.write(row, 6, campaign.request_staff or '', data_format)
                sheet.write(row, 7, campaign.turn or '', data_format)
                sheet.write(row, 8, campaign.priority or '', data_format)
                row += 1