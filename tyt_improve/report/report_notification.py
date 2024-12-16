import base64
import io
from PIL import Image
from odoo import models

class Report_excel_notification(models.AbstractModel):
    _name = 'report.report_excel_notification.xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Notificación de actualización'

    def draw_thick_border_rectangle(self, sheet, workbook, start_row, start_col, end_row, end_col):
        """Draw a rectangle with thick borders in the Excel worksheet"""
        thick_border_formats = {
            'top': workbook.add_format({'top': 2, 'top_color': '#000000'}),
            'bottom': workbook.add_format({'bottom': 2, 'bottom_color': '#000000'}),
            'left': workbook.add_format({'left': 2, 'left_color': '#000000'}),
            'right': workbook.add_format({'right': 2, 'right_color': '#000000'}),
            'top_left': workbook.add_format({'top': 2, 'left': 2, 'top_color': '#000000', 'left_color': '#000000'}),
            'top_right': workbook.add_format({'top': 2, 'right': 2, 'top_color': '#000000', 'right_color': '#000000'}),
            'bottom_left': workbook.add_format({'bottom': 2, 'left': 2, 'bottom_color': '#000000', 'left_color': '#000000'}),
            'bottom_right': workbook.add_format({'bottom': 2, 'right': 2, 'bottom_color': '#000000', 'right_color': '#000000'})
        }

        # Draw horizontal borders
        for col in range(start_col, end_col + 1):
            sheet.write_blank(start_row, col, None, thick_border_formats['top'])
            sheet.write_blank(end_row, col, None, thick_border_formats['bottom'])

        # Draw vertical borders
        for row in range(start_row, end_row + 1):
            sheet.write_blank(row, start_col, None, thick_border_formats['left'])
            sheet.write_blank(row, end_col, None, thick_border_formats['right'])

        # Draw corners
        sheet.write_blank(start_row, start_col, None, thick_border_formats['top_left'])
        sheet.write_blank(start_row, end_col, None, thick_border_formats['top_right'])
        sheet.write_blank(end_row, start_col, None, thick_border_formats['bottom_left'])
        sheet.write_blank(end_row, end_col, None, thick_border_formats['bottom_right'])

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Notificación de Actualización')
    
        # Add company logo
        logo = self.env.company.logo
        if (logo):
            image_data = base64.b64decode(logo)
            image_stream = io.BytesIO(image_data)
            image = Image.open(image_stream)
            image_width, image_height = image.size
            aspect_ratio = image_height / image_width
            new_width = 150
            new_height = int(new_width * aspect_ratio)
            sheet.insert_image('D1', 'company_logo.png', {
                'image_data': image_stream,
                'x_scale': new_width / image_width,
                'y_scale': new_height / image_height,
                'x_offset': 10
            })
    
        # Formatos
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 20,
            'font_color': 'white',
            'bg_color': '#215967',
            'align': 'center',
            'valign': 'vcenter',
            'border': 2,
            'border_color': '#000000'
        })
    
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#31879b',
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'text_wrap': True
        })

        # Add a new format specifically for left-aligned headers
        header_format_left = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#31879b',
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'text_wrap': True
        })

        # Add a new format specifically for centered headers
        header_format_center = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#31879b',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })
    
        data_format = workbook.add_format({
            'font_color': 'black',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
    
        date_format = workbook.add_format({
            'num_format': 'dd/mm/yyyy',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'black'
        })

        data_format_wrap = workbook.add_format({
            'font_color': 'black',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })
    
        # Título
        sheet.merge_range('E3:I5', 'COMUNICADO DE CAMBIOS EN PROCESO', title_format)
    
        # Fechas
        sheet.write('D8', 'Fecha de Solicitud:', header_format_left)
        sheet.write('E8', lines.request_date or '', date_format)
        sheet.write('D9', 'Fecha de Autorización:', header_format_left)
        sheet.write('E9', lines.authorization_date or '', date_format)
        sheet.write('D10', 'Fecha de Cambio:', header_format_left)
        sheet.write('E10', lines.response_date or '', date_format)
        sheet.write('D11', 'Fecha de liberación:', header_format_left)
        sheet.write('E11', lines.release_date or '', date_format)
    
        # Solicitante section
        sheet.merge_range('D15:F15', 'Solicitante', header_format_center)
        sheet.write('D16', 'Nombre', header_format)
        sheet.write('E16', 'Puesto', header_format)
        sheet.write('F16', 'Sitio', header_format)
        sheet.write('D17', lines.employee_id.name or '', data_format_wrap)
        sheet.write('E17', lines.employee_id.job_id.name or '', data_format_wrap)
        sheet.write('F17', lines.employee_id.department_id.name or '', data_format_wrap)
    
        # Autorizante section
        sheet.merge_range('H15:J15', 'Autorizante', header_format_center)
        sheet.write('H16', 'Nombre', header_format)
        sheet.write('I16', 'Puesto', header_format)
        sheet.write('J16', 'Sitio', header_format)
        sheet.write('H17', lines.responsible_id.name or '', data_format_wrap)
        sheet.write('I17', lines.responsible_id.job_id.name or '', data_format_wrap)
        sheet.write('J17', lines.responsible_id.department_id.name or '', data_format_wrap)
    
        # Procedimiento y Cláusula
        sheet.write('D21', 'Procedimiento:', header_format_left)
        sheet.merge_range('E21:G21', lines.procedures_char or '', data_format_wrap)
        sheet.write('D23', 'Cláusula:', header_format_left)
        sheet.write('E23', ', '.join(lines.clause_id.mapped('name')) if lines.clause_id else '', data_format_wrap)
    
        # Narrativa oficial
        left_format = workbook.add_format({'align': 'left', 'text_wrap': True})
        sheet.merge_range('D27:E27', 'Narrativa oficial de la cláusula', left_format)
    
        # Merged cells with border D28:J31
        border_format = workbook.add_format({'border': 1, 'text_wrap': True})
        sheet.merge_range('D28:J31', lines.clause_narrative or '', border_format)
    
        # Cambio a realizar
        sheet.write('D32', 'Cambio a realizar', left_format)
    
        # Large text section
        text_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'text_wrap': True
        })
        sheet.merge_range('D33:J37', lines.description or '', text_format)

        # Ajustar altos de filas
        sheet.set_row(12, 3.75)
        sheet.set_row(17, 3.75)
        sheet.set_row(18, 3.75)
        sheet.set_row(21, 3.75)
        sheet.set_row(24, 3.75)
        sheet.set_row(37, 3.75)
        sheet.set_row(38, 3.75)
        
        
        # Ajustar anchos de columna
        sheet.set_column('F:F', 15)
        sheet.set_column('B:C', 0.33)
        sheet.set_column('K:L', 0.33)
        sheet.set_column('D:D', 22.5)
        sheet.set_column('E:E', 22)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 15)
        sheet.set_column('J:J', 15)
        
        self.draw_thick_border_rectangle(sheet, workbook, 13, 2, 17, 10)  # Desde C14 hasta K18
        
        self.draw_thick_border_rectangle(sheet, workbook, 19, 2, 23, 10)  # Desde C20 hasta K24
        
        self.draw_thick_border_rectangle(sheet, workbook, 25, 2, 37, 10)  # Desde C26 hasta K38

        self.draw_thick_border_rectangle(sheet, workbook, 12, 1, 38, 11)  # Desde B13 hasta L39