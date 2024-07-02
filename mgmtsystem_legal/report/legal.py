import base64
import io
from collections import defaultdict

from bs4 import BeautifulSoup
from PIL import Image

from odoo import api, fields, models


class LegalPlanReport(models.AbstractModel):
    _name = 'report.mgmtsystem_legal.report_requirements_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            legal_plan_id = self.env['legal.plan'].browse(data['id'])
        else:
            legal_plan_id = self.env['legal.plan'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': legal_plan_id,
        }


class LegalPlanReportWizard(models.TransientModel):
    _name = 'legal.plan.report.wizard'

    def action_print(self):
        return self.env.ref('mgmtsystem_legal.report_announcement').report_action(self.plan_ids)

    plan_ids = fields.Many2one(
        string='Planes legales',
        comodel_name='legal.plan',
        relation='plan_legal_wizard_report_rel',
        column1='plan_id',
        column2='wizard_id',
        required=True,
    )

    def export_xls(self):
        return self.env.ref('mgmtsystem_legal.report_plan_legal_xlsx').report_action(self.plan_ids)


class ReportPlanLegal(models.AbstractModel):
    _name = 'report.mgmtsystem_legal.legal_plan'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, plans):
        format21_c_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format26_c_bold = workbook.add_format(
            {'font_size': 14, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})
        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})
        format21_gray = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        format21_gray_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, })

        format21_c_bold.set_border()
        format26_c_bold.set_border()
        format21_left.set_border()
        format21_gray.set_border()
        format21_gray_bold.set_border()

        for plan in plans:
            sheet = workbook.add_worksheet(str(plan.code)+'_Matriz legal')

            sheet.set_column(0, 0, 5)
            sheet.set_column(1, 1, 13)
            sheet.set_column(2, 2, 16)
            sheet.set_column(3, 3, 32)
            sheet.set_column(4, 4, 14)
            sheet.set_column(5, 5, 5)
            sheet.set_column(6, 7, 35)
            sheet.set_column(8, 8, 28)
            name = plan.name or ''
            sheet.merge_range(
                'A1:C3', self.env.user.company_id.name, format21_c_bold)
            sheet.merge_range('D1:H3', 'EVALUACIÓN DE MATRÍZ DE CUMPLIMIENTO DE REQUISITOS LEGALES'+'\n'
                              + name, format26_c_bold)
            code = plan.code if plan.code else ''
            sheet.write('I1', 'Código:' + code, format21_c_bold)
            datetime = fields.Datetime.now(self)
            sheet.write('I2', 'Edición: '+plan.numero, format21_c_bold)
            sheet.write('I3', 'Fecha: '+str(datetime), format21_c_bold)

            sheet.write('A4', 'Nro', format21_gray_bold)
            sheet.write('B4', 'Tipo', format21_gray_bold)
            sheet.write('C4', 'Entidad', format21_gray_bold)
            sheet.write('D4', 'Norma legal', format21_gray_bold)
            sheet.write('E4', 'Fecha de emisión', format21_gray_bold)
            sheet.write('F4', 'Art.', format21_gray_bold)
            sheet.write('G4', 'Resumen de la normativa', format21_gray_bold)
            sheet.write('H4', 'Cómo se cumplirá', format21_gray_bold)
            sheet.write('I4', 'Responsable', format21_gray_bold)

            company_id = self.env.user.company_id

            buf_image = io.BytesIO(base64.b64decode(company_id.logo))
            im = Image.open(buf_image)
            width, height = im.size
            image_width = width
            image_height = height
            cell_width = 40.1
            cell_height = 60.0

            x_scale = cell_width/image_width
            y_scale = cell_height/image_height

            print(x_scale, y_scale)

            sheet.insert_image('A1', "logo.png", {
                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})

            row = 4
            count = 0

            for line in plan.line_ids:
                count += 1
                column = 0
                sheet . set_row(row, 35)
                sheet.write(row, column, count, format21_left)
                column += 1
                sheet.write(
                    row, column, line.legal_id.type_id.name if line.legal_id.type_id else '', format21_left)
                column += 1

                value = line.legal_id.entity_id.name if line.legal_id.entity_id and hasattr(line.legal_id.entity_id, 'name') \
                    else line.legal_id.entity_id or ''

                sheet.write(row, column, value, format21_left)

                column += 1
                sheet.write(row, column, line.legal_id.name, format21_left)
                column += 1
                date_release = line.legal_id.date_release.strftime(
                    '%d/%m/%Y') if line.legal_id and line.legal_id.date_release else ''
                sheet.write(row, column, date_release, format21_left)
                column += 1
                sheet.write(row, column, len(
                    line.legal_id.article_ids), format21_left)
                column += 1
                sheet.write(row, column, BeautifulSoup(
                    line.legal_id.resume or "", 'lxml').get_text(), format21_left)
                column += 1
                sheet.write(
                    row, column, line.action_id.name if line.action_id else "No establecido", format21_left)
                column += 1
                sheet.write(row, column, line.user_id.name, format21_left)
                row += 1

            sheet2 = workbook.add_worksheet(str(plan.code)+'_Evaluación')

            sheet2.set_column(0, 0, 5)
            sheet2.set_column(1, 1, 13)
            sheet2.set_column(2, 2, 16)
            sheet2.set_column(3, 3, 32)
            sheet2.set_column(4, 4, 14)
            sheet2.set_column(5, 6, 25)
            sheet2.set_column(7, 7, 30)
            sheet2.set_column(8, 8, 24)
            name = plan.name or ''
            sheet2.merge_range(
                'A1:C3', self.env.user.company_id.name, format21_c_bold)
            sheet2.merge_range('D1:H3', 'EVALUACIÓN DE MATRÍZ DE CUMPLIMIENTO DE REQUISITOS LEGALES'+'\n'
                               + name, format26_c_bold)
            code = plan.code if plan.code else ''
            sheet2.write('I1', 'Código:' + code, format21_c_bold)
            datetime = fields.Datetime.now(self)
            sheet2.write('I2', 'Edición: '+plan.numero, format21_c_bold)
            sheet2.write('I3', 'Fecha: '+str(datetime), format21_c_bold)
            sheet2 . set_row(3, 30)
            sheet . set_row(3, 30)
            sheet2.write('A4', 'Nro', format21_gray_bold)
            sheet2.write('B4', 'Tipo', format21_gray_bold)
            sheet2.write('C4', 'Entidad', format21_gray_bold)
            sheet2.write('D4', 'Norma legal', format21_gray_bold)
            sheet2.write('E4', 'Fecha de evaluación', format21_gray_bold)
            sheet2.write('F4', 'Evaluador', format21_gray_bold)
            sheet2.write('G4', 'Resultado de la evaluación',
                         format21_gray_bold)
            sheet2.write('H4', 'Propuesta de acción', format21_gray_bold)
            sheet2.write('I4', 'Estado de la acción', format21_gray_bold)

            buf_image = io.BytesIO(base64.b64decode(
                self.env.user.company_id.logo))
            sheet2.insert_image('A1', "any_name.png", {
                                'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})

            row = 4
            count = 0
            for history in plan.history_ids:
                for line in history.line_ids:
                    count += 1
                    column = 0
                    sheet2.set_row(row, 35)
                    sheet2.write(row, column, count, format21_left)
                    column += 1
                    sheet2.write(
                        row, column, line.legal_id.type_id.name, format21_left)
                    column += 1
                    sheet2.write(
                        row, column, line.legal_id.entity_id.name, format21_left)
                    column += 1
                    sheet2.write(
                        row, column, line.legal_id.name, format21_left)
                    column += 1
                    sheet2.write(row, column, line.date_track.strftime(
                        '%d/%m/%Y') if line.date_track else '', format21_left)
                    column += 1
                    sheet2.write(row, column, line.user_id.name, format21_left)
                    column += 1
                    sheet2.write(row, column, line.result, format21_left)
                    column += 1
                    sheet2.write(
                        row, column, line.proposal_action_id.name if line.proposal_action_id else "-", format21_left)
                    column += 1
                    state_name = dict(line.proposal_action_id._fields['state'].selection).get(
                        line.proposal_action_id.state) if line.proposal_action_id else "-"
                    sheet2.write(row, column, state_name, format21_left)
                    row += 1
