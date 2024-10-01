# from odoo import fields, models, _
# from datetime import datetime
# import base64
# import io

# class ReportRemediationlanXlsx(models.AbstractModel):

#     _name = 'report.tyt_remediation_plan.remediation_report'
#     _inherit = 'report.report_xlsx.abstract'
#     _description = 'Remediacion Plan Report'

#     def generate_xlsx_report(self, workbook, data, objs):
#         title_format = workbook.add_format({
#             'bold': True, 
#             'font_size': 16, 
#             'align': 'center', 
#             'valign': 'vcenter'
#         })

#         table_header_format = workbook.add_format({
#             'bold': True, 
#             'bg_color': '#D3D3D3', 
#             'align': 'center', 
#             'valign': 'vcenter',
#             'border': 1
#         })

#         table_content_format = workbook.add_format({
#             'font_size': 10, 
#             'align': 'left', 
#             'valign': 'vcenter',
#             'border': 1
#         })
        
    

#         remediation_plan = objs[0] 
#         sheet = workbook.add_worksheet('Hoja Costo de Importaciónes')
#         sheet.hide_gridlines(option=2)

#         # Definir tamaño de las columnas (anchura)
#         sheet.set_column('A:A', 5)  # Columna A con un ancho de 30
#         sheet.set_column('B:B', 30) 
#         sheet.set_column('C:C', 30)
#         sheet.set_column('D:D', 20)
#         sheet.set_column('E:E', 15) 
#         sheet.set_column('F:F', 20)
#         sheet.set_column('G:G', 30)
        

#         # Definir tamaño de las filas (altura)
#         sheet.set_row(0, 40) 
#         sheet.set_row(1, 20) 

        
#         if remediation_plan.company_id.logo:
#             logo_data = base64.b64decode(remediation_plan.company_id.logo)
#             image_stream = io.BytesIO(logo_data)
#             sheet.insert_image('B2', 'logo.png', {'image_data': image_stream, 'x_scale': 2.5, 'y_scale': 2.5}) 
            
#         sheet.write('C2:F2', 'PLAN DE REMEDIACIÓN', title_format)
        
        # # Cabecera 
        # sheet.set_row(4, 15)
        # sheet.write('B4', 'Remediation Area', table_header_format)
        # sheet.write('C4', 'Activity', table_header_format)
        # sheet.write('D4', 'Execution Priority', table_header_format)
        # sheet.write('E4', 'Execution Date', table_header_format)
        # sheet.write('F4', 'Evidence', table_header_format)
        # sheet.write('G4', 'Resourses', table_header_format)
        
        # row = 4
        
        # for plan in remediation_plan.remediation_plan_line_ids:
        #     sheet.write(row, 1, plan.remediation_area, table_content_format)
        #     sheet.write(row, 2, plan.activity, table_content_format)
        #     sheet.write(row, 3, plan.execution_priority, table_content_format)
        #     sheet.write(row, 4, plan.execution_date, table_content_format)
        #     sheet.write(row, 5, plan.evidence, table_content_format)
        #     sheet.write(row, 6, plan.resourses, table_content_format)
        #     sheet.set_row(row, 10)
        #     row += 1
            