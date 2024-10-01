from odoo import fields, models, _
from datetime import datetime
import base64
import io

class ReportRemediationLogXlsx(models.AbstractModel):

	_name = 'report.tyt_remediation_log.remediation_report'
	_inherit = 'report.report_xlsx.abstract'
	_description = 'Remediacion Log Report'

	def generate_xlsx_report(self, workbook, data, objs):
		title_format = workbook.add_format({
		'bold': True, 
		'font_size': 16, 
		'align': 'center', 
		'valign': 'vcenter'
		})

		table_header_format = workbook.add_format({
		'bold': True, 
		'bg_color': '#D3D3D3', 
		'align': 'center', 
		'valign': 'vcenter',
		'border': 1
		})

		table_content_format = workbook.add_format({
		'font_size': 10, 
		'align': 'left', 
		'valign': 'vcenter',
		'border': 1
		})
		signature_format = workbook.add_format({
		'border': 0,   # Desactivar los bordes por defecto
		'top': 1,      # Activar solo el borde superior
		'font_size': 10, 
		'align': 'left', 
		'valign': 'vcenter',
		})
		


		remediation_log = objs[0] 
		sheet = workbook.add_worksheet('Hoja Costo de Importaciónes')
		sheet.hide_gridlines(option=2)

		# Definir tamaño de las columnas (anchura)
		sheet.set_column('A:A', 5)  # Columna A con un ancho de 30
		sheet.set_column('B:B', 5) 
		sheet.set_column('C:C', 30)
		sheet.set_column('D:D', 20)
		sheet.set_column('E:E', 20) 
		sheet.set_column('F:F', 20)
		sheet.set_column('G:G', 20)
		sheet.set_column('H:H', 20) 
		sheet.set_column('I:I', 20)
		sheet.set_column('J:J', 20)
		

		# Definir tamaño de las filas (altura)
		sheet.set_row(0, 5) 
		sheet.set_row(1, 40) 
		
		if remediation_log.company_id.logo:
			logo_data = base64.b64decode(remediation_log.company_id.logo)
			image_stream = io.BytesIO(logo_data)
			sheet.insert_image('C2:J2', 'logo.png', {'image_data': image_stream, 'x_scale': 2.5, 'y_scale': 2.5}) 
		
		sheet.write('D2', 'Bitacora de Remediación', title_format)
		
		# ============== Recepcion =================
		sheet.set_row(5, 40) 
		sheet.set_row(6, 40) 
		sheet.write('C5', 'Recepcion', table_header_format)
		reception_detection_text = 'Deteccion: ' + remediation_log.remediation_log_line_ids[0].detection 
		sheet.write('D5:J5',reception_detection_text , table_content_format)
		
		sheet.write('C6', 'Recepcion', table_header_format)
		reception_remediation_text = '¿Que se realizo?: ' + remediation_log.remediation_log_line_ids[0].remediation 
		sheet.write('D5:J5',reception_remediation_text , table_content_format)

		# ============== Salas =================
		sheet.set_row(11, 40) 
		sheet.set_row(12, 40) 
		sheet.write('C11', 'Salas', table_header_format)
		halls_detection_text = 'Deteccion: ' + remediation_log.remediation_log_line_ids[1].detection 
		sheet.write('D11:J11',halls_detection_text , table_content_format)
		
		sheet.write('C12', 'Salas', table_header_format)
		halls_remediation_text = '¿Que se realizo?: ' + remediation_log.remediation_log_line_ids[1].remediation 
		sheet.write('D12:J12',halls_remediation_text , table_content_format)
		
		# ============== Operaciones =================
		sheet.set_row(17, 40) 
		sheet.set_row(18, 40) 
		sheet.write('C17', 'Operaciones', table_header_format)
		reception_detection_text = 'Deteccion: ' + remediation_log.remediation_log_line_ids[2].detection 
		sheet.write('D17:J17',reception_detection_text , table_content_format)
		
		sheet.write('C18', 'Operaciones', table_header_format)
		reception_remediation_text = '¿Que se realizo?: ' + remediation_log.remediation_log_line_ids[2].remediation 
		sheet.write('D18:J18',reception_remediation_text , table_content_format)
		
		# ============== Of. Administrativas =================
		sheet.set_row(23, 40) 
		sheet.set_row(24, 40) 
		sheet.write('C23', 'Of. Administrativas', table_header_format)
		admin_detection_text = 'Deteccion: ' + remediation_log.remediation_log_line_ids[3].detection 
		sheet.write('D23:J23',admin_detection_text , table_content_format)
		
		sheet.write('C24', 'Of. Administrativas', table_header_format)
		admin_remediation_text = '¿Que se realizo?: ' + remediation_log.remediation_log_line_ids[3].remediation 
		sheet.write('D24:J24',admin_remediation_text , table_content_format)
		
		# ============== Baños  =================
		sheet.set_row(29, 40) 
		sheet.set_row(30, 40) 
		sheet.write('C29', 'Baños', table_header_format)
		br_detection_text = 'Deteccion: ' + remediation_log.remediation_log_line_ids[4].detection 
		sheet.write('D29:J29',br_detection_text , table_content_format)
		
		sheet.write('C30', 'Baños', table_header_format)
		br_remediation_text = '¿Que se realizo?: ' + remediation_log.remediation_log_line_ids[4].remediation 
		sheet.write('D30:J30',br_remediation_text , table_content_format)
		
		# ============== Loker  =================
		sheet.set_row(35, 40) 
		sheet.set_row(36, 40) 
		sheet.write('C35', 'Loker', table_header_format)
		loker_detection_text = 'Deteccion: ' + remediation_log.remediation_log_line_ids[5].detection 
		sheet.write('D35:J35',loker_detection_text , table_content_format)
		
		sheet.write('C36', 'Loker', table_header_format)
		loker_remediation_text = '¿Que se realizo?: ' + remediation_log.remediation_log_line_ids[5].remediation 
		sheet.write('D36:J36',loker_remediation_text , table_content_format)
		
		sheet.set_row(39, 50) 
		sheet.write('C39', 'Observaciones', table_header_format) 
		sheet.write('D39:J39',remediation_log.observations  , table_content_format)
		
		sheet.write('C45', 'Firma Mantenimiento', signature_format)
		sheet.write('E45', 'Firma de Seguridad', signature_format)
		sheet.write('G45', 'Firma TI', signature_format)
		sheet.write('I45', 'Firma Gerente de Sitio', signature_format)