from odoo import fields, models, _
from datetime import datetime
from math import modf
import base64
import io

class ReportQualityPlanXlsx(models.AbstractModel):

    _name = 'report.tyt_quality_plan.quality_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Quality Plan Report'

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
        
        # Format for the headers
        sub_header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#B7DEE8',
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
        
        # Format for the data
        data_bold_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'align': 'left',
            'valign': 'vcenter',
            'border': 2,
            'text_wrap': True,
            'border_color': '#757070',
        })
        
        # Format for the data
        s_data_format = workbook.add_format({
            'font_size': 12,
            'align': 'left',
            'valign': 'vcenter',
            'text_wrap': True,
        })
        
        # Format for the data
        s_data_bold_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'align': 'right',
            'valign': 'vcenter',
            'text_wrap': True,
        })
        # Format for the signature
        signature_format = workbook.add_format({
			'border': 0,   # Desactivar los bordes por defecto
			'top': 1,      # Activar solo el borde superior
			'font_size': 12, 
			'align': 'center', 
			'valign': 'vcenter',
		})

        quality_plan = objs[0] 
        sheet = workbook.add_worksheet('Plan de Quality')
        sheet.hide_gridlines(option=2)

        # Definir tamaño de las columnas (anchura)
        sheet.set_column('A:A', 5)  
        sheet.set_column('B:B', 50) 
        sheet.set_column('C:C', 1)
        sheet.set_column('D:D', 50)
        sheet.set_column('E:E', 1) 
        sheet.set_column('F:F', 50)
        sheet.set_column('G:G', 30)
        sheet.set_column('H:H', 1)
        sheet.set_column('I:I', 40)
        sheet.set_column('J:J', 5)

        # Definir tamaño de las filas (altura)
        sheet.set_row(0, 20) 
        sheet.set_row(1, 10) 
        sheet.set_row(2, 10) 
        sheet.set_row(3, 30) 
        
        if quality_plan.company_id.logo:
            logo_data = base64.b64decode(quality_plan.company_id.logo)
            image_stream = io.BytesIO(logo_data)
            sheet.insert_image('B2', 'logo.png', {'image_data': image_stream, 'x_scale': 1.0, 'y_scale': 1.5}) 
            
        sheet.merge_range('C2:F4', 'PLAN DE MANTENIMIENTO', title_format)
        
        sheet.write('G2', 'Semana:', s_data_bold_format)
        sheet.write('I2', quality_plan.week or '', s_data_format)
        
        sheet.write('G3', 'Sitio:', s_data_bold_format)
        sheet.write('I3', quality_plan.site.x_name or '', s_data_format)
        
        # Cabecera 
        sheet.set_row(6, 15)
        sheet.write('B7', 'VERIFICACIÓN', header_format)
        sheet.write('D7', 'CONTROL', header_format)
        sheet.write('F7', 'MONITOREO', header_format)
        sheet.write('G7', 'MEDICIÓN', header_format)
        sheet.write('I7', 'CUMPLIMIENTO', header_format)
        
        row = 7
        
        for plan in quality_plan.quality_plan_line_ids:
            sheet.set_row(row-1, 15) 
            sheet.write(row, 3, plan.control or '', data_format)
            sheet.write(row, 5, plan.monitoring or '', data_format)
            sheet.write(row, 6, '{}%'.format((plan.percentage or 0) * 100), data_format)
            
            sheet.write(row, 8, plan.status or '', data_format)
            row += 1
            
            
        sheet.merge_range('B8:B{}'.format(row), 'Validación de bitácora de remediación vs plan', data_format)
        
        row += 2
        sheet.write(row, 6, 'Evaluación:', sub_header_format)
        sheet.write(row, 8, '{}%'.format((quality_plan.total_percentage or 0) * 100), data_bold_format)
        
        # ============== Observaciones  =================
        row += 4
        sheet.write('D{}'.format(row), 'COMENTARIOS DE RETROALIMENTACIÓN:', sub_header_format) 
        
        row += 1
        sheet.merge_range('D{}:F{}'.format(row,row+4),quality_plan.observations or '' , data_format)
		
        # ============== Firma  =================
        row += 9
        sheet.write(row, 1, 'Auxiliar de Mantenimiento', signature_format)
        sheet.write(row, 3, 'Soporte tecnico de TI', signature_format)
        sheet.write(row, 5, 'Gerente de Sitio', signature_format)