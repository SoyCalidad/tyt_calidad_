from odoo import models 

import logging 

_logger = logging.getLogger(__name__)

class CustomizedReportWizard(models.AbstractModel):
    _name = 'report.tyt_risk_management.customized_report_wizard_template'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Customized Report Template"

    def generate_xlsx_report(self, workbook, data, records):
        title_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'border': 1,
            'bg_color': '#BFBFBF',
        })

        text_format = workbook.add_format({
            'border': 1,
        })
        number_format = workbook.add_format({
            'border': 1,
            'align': 'end',
        })
        for rec in records:
            data_xlsx = self.env['tyt.risk.mitigation'].customized_report(
                department_ids=rec.department_ids.ids, 
                pdomain_ids=rec.pdomain_ids.ids, 
                process_ids=rec.process_ids.ids, 
                years=rec.years.split(",") if rec.years else [], 
                months=rec.months.split(",") if rec.months else [],
            )
            sheet = workbook.add_worksheet('Reporte')

            _logger.info(f'labeltiems, {data_xlsx.get("label_time", [])}')
            for index, time in enumerate(data_xlsx.get("label_time", [])):
                sheet.merge_range(0,4 + index * 3, 0, 4 +index * 3 +2, time, title_format )

            sheet.write(1,0, "Sitio", title_format)
            sheet.write(1,1, "Proceso", title_format)
            sheet.write(1,2, "Sub Proceso", title_format)
            sheet.write(1,3, "Dominio", title_format)
            sheet.set_column(0, 3, 25)

            for index, label in enumerate(data_xlsx.get("label_header", [])):
                sheet.write(1,4+index, label, title_format)

            sheet.set_column(4, 4+len(data_xlsx.get("label_header", [])), 25)

            row = 2
            for d in data_xlsx.get("list", []):
                sheet.write(row, 0, d.get("department_name", ""), text_format)
                sheet.write(row, 1, d.get("process_name", ""), text_format)
                sheet.write(row, 2, d.get("sub_process_name", ""), text_format)
                sheet.write(row, 3, d.get("pdomain_name", ""), text_format)

                for index, month_value in enumerate(d.get("month_table", [])):
                    sheet.write(row, 4 + index*3 , month_value.get("cantidad", ""), text_format)
                    sheet.write(row, 4 + index*3 +1 , f'{month_value.get("compliance", "")} %', text_format)
                    sheet.write(row, 4 + index*3 +2 , f'{month_value.get("complianceAcomulado", "")} %', text_format)

                row += 1

        
class AccumulatedCustomizedReportWizard(models.AbstractModel):
    _name = 'report.tyt_risk_management.accumulated_customized_template'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Accumulated Customized Report Template"

    def generate_xlsx_report(self, workbook, data, records):
        title_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'border': 1,
            'bg_color': '#BFBFBF',
        })

        text_format = workbook.add_format({
            'border': 1,
        })
        number_format = workbook.add_format({
            'border': 1,
            'align': 'end',
        })
        for rec in records:
            domain_mitigation = []
            if rec.department_ids.ids:
                domain_mitigation.append(('risk_id.department_id', 'in', rec.department_ids.ids))
            if rec.pdomain_ids.ids:
                domain_mitigation.append(('risk_id.pdomain_id', 'in', rec.pdomain_ids.ids))
            if rec.process_ids.ids:
                domain_mitigation.append(('risk_id.process_id', 'in', rec.process_ids.ids))
            if rec.years:
                domain_mitigation.append(('year', 'in', rec.years.split(",")))
            if rec.months:
                domain_mitigation.append(('month', 'in', rec.months.split(",")))

            mitigations = self.env['tyt.risk.mitigation'].search(domain_mitigation)
            sheet = workbook.add_worksheet('Data')

            headers = [
                "ID Riesgo",
                "Dominio",
                "Año",
                "Mes",
                "Revisión",
                "Sitio",
                "Categoría del Estado Financiero",
                "Objetivo COSO",
                "Proceso",
                "Sub Proceso",
                "Riesgo asociado",
                "Objetivo de Control",
                "Estatus de Mitigación",
                "Dueño del proceso",
                "Dueño del control",
                "Revisor",
                "Estatus de Monitoreo %",
                "Periodo de revisión",
                "Auditor",
            ]

            for col, header in enumerate(headers):
                sheet.write(0, col, header, title_format)


            		

            sheet.set_column(0, len(headers), 25)
            dict_months = dict(self.env['tyt.risk.mitigation']._fields['month'].selection)
            dict_cr_period = dict(self.env['tyt.risk.management']._fields['cr_peoriod'].selection)

            row = 1
            for mitigation in mitigations:
                sheet.write(row, 0, mitigation.risk_id_id, text_format)
                sheet.write(row, 1, mitigation.risk_id_pdomain_id.name or '', text_format)
                sheet.write(row, 2, mitigation.year, text_format)
                sheet.write(row, 3, dict_months.get(mitigation.month), text_format)
                sheet.write(row, 4, "", text_format)
                sheet.write(row, 5, mitigation.risk_id_department_id.name or '', text_format)
                sheet.write(row, 6,  '', text_format)
                sheet.write(row, 7, ",".join([g.name for g in mitigation.risk_id.goal_coso_ids]),  text_format)
                sheet.write(row, 8, mitigation.risk_id_process_id.name or '', text_format)
                sheet.write(row, 9, mitigation.risk_id_subprocess_id.name or '', text_format)
                sheet.write(row, 10, mitigation.risk_id.name or '', text_format)
                sheet.write(row, 11, mitigation.risk_id.control_objective or '', text_format)
                sheet.write(row, 12, mitigation.mr_degree_mitigation.name or '', text_format)
                sheet.write(row, 13, mitigation.risk_id.process_id.owner_id.display_name or '', text_format)
                sheet.write(row, 14, mitigation.risk_id_owner_id.display_name or '', text_format)
                sheet.write(row, 15, mitigation.risk_id_reviewer_id.display_name or '', text_format)
                sheet.write(row, 16, mitigation.ma_degree_mitigation.display_name or '', text_format)
                sheet.write(row, 17, dict_cr_period.get(mitigation.risk_id.cr_peoriod, '' ) or '', text_format)
                sheet.write(row, 18, mitigation.risk_id_auditor_id.display_name or '', text_format)

                row += 1

        

