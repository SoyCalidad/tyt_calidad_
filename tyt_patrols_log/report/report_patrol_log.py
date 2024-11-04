from odoo import fields, models, _
from datetime import datetime
import base64
import io

class ReportPatrolLogXlsx(models.AbstractModel):

	_name = 'report.tyt_patrol_log.patrol_report'
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
  
		# Format for the Observations
		obs_format = workbook.add_format({
			'font_size': 12,
			'align': 'left',
			'valign': 'vcenter',
			'text_wrap': True,
		})

  		# Format for the Observations
		obst_format = workbook.add_format({
			'bold': True,
			'font_size': 12,
			'align': 'center',
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
		


		patrol_log = objs[0] 
		sheet = workbook.add_worksheet('Bitacora de Rondines')
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
		
		if patrol_log.company_id.logo:
			logo_data = base64.b64decode(patrol_log.company_id.logo)
			image_stream = io.BytesIO(logo_data)
			sheet.insert_image('C2', 'logo.png', {'image_data': image_stream, 'x_scale': 0.5, 'y_scale': 0.5}) 
		
		sheet.merge_range('D2:J2', 'Bitacora de Recorridos', title_format)
		
  		# ============== Recepcion =================
		sheet.set_row(4, 50) 
		sheet.write('C5', 'Recepcion', header_format)
		sheet.merge_range('D5:J5', patrol_log.patrol_log_line_ids[0].description or ''  , data_format)
		
		# ============== Salas =================
		sheet.set_row(9, 50) 
		sheet.write('C10', 'Salas', header_format)
		sheet.merge_range('D10:J10',patrol_log.patrol_log_line_ids[1].description or '' , data_format)
		
		# ============== Operaciones =================
		sheet.set_row(14, 50) 
		sheet.write('C15', 'Operaciones', header_format)
		sheet.merge_range('D15:J15',patrol_log.patrol_log_line_ids[2].description or '' , data_format)
		
		# ============== Of. Administrativas =================
		sheet.set_row(19, 50) 
		sheet.write('C20', 'Of. Administrativas', header_format)
		sheet.merge_range('D20:J20', patrol_log.patrol_log_line_ids[3].description or '' , data_format)
		
		# ============== Baños  =================
		sheet.set_row(24, 50) 
		sheet.write('C25', 'Baños', header_format)
		sheet.merge_range('D25:J25',patrol_log.patrol_log_line_ids[4].description or '' , data_format)
		
		# ============== Loker  =================
		sheet.set_row(29, 50) 
		sheet.write('C30', 'Loker', header_format)
		sheet.merge_range('D30:J30',patrol_log.patrol_log_line_ids[5].description or '' , data_format)
		
		# ============== Observaciones  =================
		sheet.set_row(34, 50) 
		sheet.write('C35', 'Observaciones', obst_format) 
		sheet.merge_range('D35:J35',patrol_log.observations or '' , obs_format)
		
		
		sheet.write('D45', 'Guardia de Seguridad', signature_format)
		sheet.write('H45', 'Soporte Técnico de TI', signature_format)
		sheet.write('J45', 'Gerente de Sitio', signature_format)