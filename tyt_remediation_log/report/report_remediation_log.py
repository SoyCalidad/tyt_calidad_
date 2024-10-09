from odoo import fields, models, _
from datetime import datetime
import base64
import io

class ReportRemediationLogXlsx(models.AbstractModel):

	_name = 'report.tyt_remediation_log.remediation_report'
	_inherit = 'report.report_xlsx.abstract'
	_description = 'Remediacion Log Report'

	def generate_xlsx_report(self, workbook, data, objs):
		# Format for the main title
		title_format = workbook.add_format({
			'bold': True,
			'font_size': 30,
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
		# Format for the signature
		signature_format = workbook.add_format({
			'border': 0,   # Desactivar los bordes por defecto
			'top': 1,      # Activar solo el borde superior
			'font_size': 12, 
			'align': 'center', 
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
		sheet.set_row(1, 50) 
		
		if remediation_log.company_id.logo:
			logo_data = base64.b64decode(remediation_log.company_id.logo)
			image_stream = io.BytesIO(logo_data)
			sheet.insert_image('C2', 'logo.png', {'image_data': image_stream, 'x_scale': 0.5, 'y_scale': 0.5}) 
		
		sheet.merge_range('D2:J2', 'Bitacora de Remediación', title_format)
		# ============== Recepcion =================
		sheet.set_row(5, 40) 
		sheet.set_row(6, 40) 
		sheet.write('C5', 'Recepcion', header_format)
		reception_detection_text = 'Deteccion: ' + (remediation_log.remediation_log_line_ids[0].detection or '' )
		sheet.merge_range('D5:J5',reception_detection_text , data_format)
		
		sheet.write('C6', 'Recepcion', header_format)
		reception_remediation_text = '¿Que se realizo?: ' + (remediation_log.remediation_log_line_ids[0].remediation or '')
		sheet.merge_range('D5:J5',reception_remediation_text , data_format)

		# ============== Salas =================
		sheet.set_row(11, 40) 
		sheet.set_row(12, 40) 
		sheet.write('C11', 'Salas', header_format)
		halls_detection_text = 'Deteccion: ' + (remediation_log.remediation_log_line_ids[1].detection or '' )
		sheet.merge_range('D11:J11',halls_detection_text , data_format)
		
		sheet.write('C12', 'Salas', header_format)
		halls_remediation_text = '¿Que se realizo?: ' + (remediation_log.remediation_log_line_ids[1].remediation or '')
		sheet.merge_range('D12:J12',halls_remediation_text , data_format)
		
		# ============== Operaciones =================
		sheet.set_row(17, 40) 
		sheet.set_row(18, 40) 
		sheet.write('C17', 'Operaciones', header_format)
		reception_detection_text = 'Deteccion: ' + (remediation_log.remediation_log_line_ids[2].detection or '')
		sheet.merge_range('D17:J17',reception_detection_text , data_format)
		
		sheet.write('C18', 'Operaciones', header_format)
		reception_remediation_text = '¿Que se realizo?: ' + (remediation_log.remediation_log_line_ids[2].remediation or '')
		sheet.merge_range('D18:J18',reception_remediation_text , data_format)
		
		# ============== Of. Administrativas =================
		sheet.set_row(23, 40) 
		sheet.set_row(24, 40) 
		sheet.write('C23', 'Of. Administrativas', header_format)
		admin_detection_text = 'Deteccion: ' + (remediation_log.remediation_log_line_ids[3].detection or '')
		sheet.merge_range('D23:J23',admin_detection_text , data_format)
		
		sheet.write('C24', 'Of. Administrativas', header_format)
		admin_remediation_text = '¿Que se realizo?: ' + (remediation_log.remediation_log_line_ids[3].remediation or '')
		sheet.merge_range('D24:J24',admin_remediation_text , data_format)
		
		# ============== Baños  =================
		sheet.set_row(29, 40) 
		sheet.set_row(30, 40) 
		sheet.write('C29', 'Baños', header_format)
		br_detection_text = 'Deteccion: ' + (remediation_log.remediation_log_line_ids[4].detection or '')
		sheet.merge_range('D29:J29',br_detection_text , data_format)
		
		sheet.write('C30', 'Baños', header_format)
		br_remediation_text = '¿Que se realizo?: ' + (remediation_log.remediation_log_line_ids[4].remediation or '')
		sheet.merge_range('D30:J30',br_remediation_text , data_format)
		
		# ============== Loker  =================
		sheet.set_row(35, 40) 
		sheet.set_row(36, 40) 
		sheet.write('C35', 'Loker', header_format)
		loker_detection_text = 'Deteccion: ' + (remediation_log.remediation_log_line_ids[5].detection or '')
		sheet.merge_range('D35:J35',loker_detection_text , data_format)
		
		sheet.write('C36', 'Loker', header_format)
		loker_remediation_text = '¿Que se realizo?: ' + (remediation_log.remediation_log_line_ids[5].remediation or '')
		sheet.merge_range('D36:J36',loker_remediation_text , data_format)
		
		sheet.set_row(39, 50) 
		sheet.write('C39', 'Observaciones', header_format) 
		sheet.merge_range('D39:J39',remediation_log.observations or '' , data_format)
		
		sheet.write('C45', 'Firma Mantenimiento', signature_format)
		sheet.write('E45', 'Firma de Seguridad', signature_format)
		sheet.write('G45', 'Firma TI', signature_format)
		sheet.write('I45', 'Firma Gerente de Sitio', signature_format)