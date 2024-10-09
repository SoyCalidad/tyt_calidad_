from odoo import fields, models, _
from datetime import datetime
from math import modf
import base64
import io

class ReportRemediationlanXlsx(models.AbstractModel):

    _name = 'report.tyt_remediation_plan.remediation_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Remediacion Plan Report'

    def generate_xlsx_report(self, workbook, data, objs):
        # Format for the main title
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 30,
            'font_color': 'white',
            'bg_color': '#31879b',
            'align': 'center',
            'valign': 'vcenter',
            'border': 2,
            'border_color': '#757070',
        })

        # Format for the headers
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'font_color': 'white',
            'bg_color': '#31879b',
            'align': 'center',
            'valign': 'vcenter',
            'border': 2,
            'text_wrap': True,
            'border_color': '#757070',
        })

        # Format for the data
        data_format = workbook.add_format({
            'font_size': 12,
            'align': 'left',
            'valign': 'vcenter',
            'border': 2,
            'text_wrap': True,
            'border_color': '#757070',
        })

        # Formato para fechas (dd/mm/yyyy)
        date_format = workbook.add_format({
            'font_size': 12,
            'align': 'left',
            'valign': 'vcenter',
            'border': 2,
            'text_wrap': True,
            'border_color': '#757070',
            'num_format': 'dd/mm/yyyy',
        })

        remediation_plan = objs[0] 
        sheet = workbook.add_worksheet('Hoja Costo de Importaciónes')
        sheet.hide_gridlines(option=2)

        # Definir tamaño de las columnas (anchura)
        sheet.set_column('A:A', 5)  
        sheet.set_column('B:B', 30) 
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 15) 
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 30)
        

        # Definir tamaño de las filas (altura)
        sheet.set_row(0, 40) 
        sheet.set_row(1, 50) 

        
        if remediation_plan.company_id.logo:
            logo_data = base64.b64decode(remediation_plan.company_id.logo)
            image_stream = io.BytesIO(logo_data)
            sheet.insert_image('B2', 'logo.png', {'image_data': image_stream, 'x_scale': 0.5, 'y_scale': 0.5}) 
            
        sheet.merge_range('C2:G2', 'PLAN DE REMEDIACIÓN', title_format)
        
        # Cabecera 
        sheet.set_row(4, 15)
        sheet.write('B4', 'Área de Remediación', header_format)
        sheet.write('C4', 'Actividad', header_format)
        sheet.write('D4', 'Prioridad de Ejecución', header_format)
        sheet.write('E4', 'Fecha de Ejecución', header_format)
        sheet.write('F4', 'Evidencia', header_format)
        sheet.write('G4', 'Recursos', header_format)
        
        row = 4
        
        for plan in remediation_plan.remediation_plan_line_ids:
            sheet.set_row(row, 15) 
            sheet.write(row, 1, plan.remediation_area or '', data_format)
            sheet.write(row, 2, plan.activity or '', data_format)
            
            hours = int(plan.execution_priority)
            minutes = round((plan.execution_priority - hours) * 60)
            if plan.execution_priority:
                if minutes == 0:
                    execution_time_excel = str(hours) + ":00"
                else:
                    execution_time_excel = str(hours) + ":" + str(minutes).zfill(2)
            else:
                execution_time_excel = ''
            
            sheet.write(row, 3, execution_time_excel, data_format)  
            sheet.write(row, 4, plan.execution_date or '', date_format)
            sheet.write(row, 5, plan.evidence or '', data_format)
            sheet.write(row, 6, plan.resourses or '', data_format)
            
            row += 1
            