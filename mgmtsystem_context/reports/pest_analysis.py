# -*- coding: utf-8 -*-

import base64
import io
import time
from collections import defaultdict
from PIL import Image
from odoo import _, api, models
from odoo.exceptions import UserError

_TERM = {
    False : '',
    'short': 'Corto plazo',
    'medium': 'Mediano plazo',
    'large': 'Largo plazo',
}

_CALI = {
    False: '',
    'v_negative': 'Muy negativo',
    'negative': 'Negativo',
    'indifferent': 'Indiferente',
    'positive': 'Positivo',
    'v_positive': 'Muy positivo',
}


class AMOFITHPESTXLSReport(models.AbstractModel):
    _name = 'report.mgmtsystem_context.report_xls_pest'

    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        """Generate a xls report with the data

        Arguments:
            workbook {object} -- A object that represents a Excel workbook
            data {dict} -- The data of the report
            partners {object} -- A class object
        """

        if data and data.get('is_wizard'):
            partners = self.env['mgmtsystem.context.pest'].browse(
                data['pestel'])
        
        

        format_title = workbook.add_format(
            {'font_size': 15, 'bg_color': '#D3D3D3', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True,'border': 1})
        format_title1 = workbook.add_format(
            {'font_size': 13, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True,'border': 1})
        format_data = workbook.add_format(
            {'font_size': 9, 'font_name': 'Arial', 'text_wrap': True, 'border': 1})
        format_header = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 1, 'bg_color': '#D3D3D3'})

        sheet = workbook.add_worksheet('Analisis')
        company_id = self.env.user.company_id

        buf_image = io.BytesIO(base64.b64decode(company_id.logo))
        im = Image.open(buf_image)
        width, height = im.size
        image_width = width
        image_height = height
        cell_width = 48.0
        cell_height = 48.0

        x_scale = cell_width/image_width
        y_scale = cell_height/image_height
        sheet.insert_image('A1', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})


        sheet.set_column('A:A', 20)
        sheet.set_column('C:D', 20)
        sheet.set_column('E:F', 40)
        sheet.set_column('B:B', 50)

        groups1 = defaultdict(list)
        groups2 = defaultdict(list)

        for obj in partners:
            if obj.custom_analysis:
                for each in obj.internal_factor_ids:
                    groups1[each.type_id].append(each)
                for each in obj.internal_factor_ids:
                    groups2[each.type_id].append(each)
            else:
                for each in obj.admin_factor_ids + obj.marketing_factor_ids + obj.logistic_factor_ids + obj.accounting_factor_ids + obj.rrhh_factor_ids + obj.it_factor_ids + obj.internal_factor_ids:
                    groups1[each.type_id].append(each)
                for each in obj.politic_factor_ids + obj.economic_factor_ids + obj.sociocult_factor_ids + obj.tech_factor_ids + obj.ecologic_factor_ids + obj.legal_factor_ids:
                    groups2[each.type_id].append(each)

        custom_pest1 = groups1.values()
        custom_pest2 = groups2.values()

        # sheet.merge_range(0, 0, 1, 0, '')
        sheet.merge_range(0, 0, 2, 3, 'ANÁLISIS PESTEL/AMOFHIT', format_title)
        sheet.write(0, 4, 'Código: %s' % partners.code, format_header)
        
        sheet.write(1, 4, 'Versión: %s' % partners.version, format_header)
        sheet.write(2, 4, 'Fecha de elaboración: %s' %
                    (partners.date_elaborate), format_header)

        row = 4
        sheet.merge_range(3, 0, 3, 4, 'ANÁLISIS PESTEL', format_title1)
        #sheet.write(row, 0, 'CUESTIÓN', format_header)
        sheet.write(row, 0, 'DETALLE', format_header)
        sheet.write(row, 1, 'CALIFICACIÓN', format_header)
        sheet.write(row, 2, 'PLAZO', format_header)
        sheet.write(row, 3, 'RIESGO', format_header)
        sheet.write(row, 4, 'OPORTUNIDAD', format_header)
        row += 1
        for each in custom_pest2:
            sheet.merge_range(
                row, 0, row, 4, each[0].type_id.name, format_header)
            row += 1
            for factor in each:
                #sheet.write(row, 0, factor.name, format_data)
                sheet.write(
                    row, 0, factor.details if factor.details else '', format_data)
                sheet.write(row, 1, _CALI[factor.calification], format_data)
                sheet.write(row, 2, _TERM[factor.term], format_data)
                sheet.write(row, 3, '\n'.join(
                    ['- ' + x.name for x in factor.risk_ids]), format_data)
                sheet.write(row, 4, '\n'.join(
                    ['- ' + x.name for x in factor.opportunity_ids]), format_data)
                l = max(len(factor.opportunity_ids), len(factor.risk_ids))
                if l > 0:
                    sheet.set_row(row, 30*l)
                else:
                    sheet.set_row(row, 60)
                row += 1

        row += 0
        sheet.merge_range(row, 0, row, 4, 'ANÁLISIS AMOFHIT', format_title1)
        row += 1
        #sheet.write(row, 0, 'CUESTIÓN', format_header)
        sheet.write(row, 0, 'DETALLE', format_header)
        sheet.write(row, 1, 'CALIFICACIÓN', format_header)
        sheet.write(row, 2, 'PLAZO', format_header)
        sheet.write(row, 3, 'RIESGO', format_header)
        sheet.write(row, 4, 'OPORTUNIDAD', format_header)
        row += 1
        for each in custom_pest1:
            sheet.merge_range(
                row, 0, row, 4, each[0].type_id.name, format_header)
            row += 1
            for factor2 in each:
                #sheet.write(row, 0, factor2.name, format_data)
                sheet.write(
                    row, 0, factor2.details if factor2.details else '', format_data)
                sheet.write(row, 1, _CALI[factor2.calification], format_data)
                sheet.write(row, 2, _TERM[factor2.term], format_data)
                sheet.write(row, 3, '\n'.join(
                    ['- ' + x.name for x in factor2.risk_ids]), format_data)
                sheet.write(row, 4, '\n'.join(
                    ['- ' + x.name for x in factor2.opportunity_ids]), format_data)
                l = max(len(factor2.opportunity_ids), len(factor2.risk_ids))
                if l > 0:
                    sheet.set_row(row, 20*l)
                else:
                    sheet.set_row(row, 25)
                row += 1

        workbook.close()


class AMOFITHPESTReport(models.AbstractModel):
    _name = 'report.mgmtsystem_context.report_pest'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            docs = self.env['mgmtsystem.context.pest'].browse(data['pestel'])
        else:
            docs = self.env['mgmtsystem.context.pest'].browse(docids)

        groups1 = defaultdict(list)
        groups2 = defaultdict(list)

        for obj in docs:
            if obj.custom_analysis:
                for each in obj.internal_factor_ids:
                    groups1[each.type_id].append(each)
                for each in obj.internal_factor_ids:
                    groups2[each.type_id].append(each)
            else:
                for each in obj.admin_factor_ids + obj.marketing_factor_ids + obj.logistic_factor_ids + obj.accounting_factor_ids + obj.rrhh_factor_ids + obj.it_factor_ids + obj.internal_factor_ids:
                    groups1[each.type_id].append(each)
                for each in obj.politic_factor_ids + obj.economic_factor_ids + obj.sociocult_factor_ids + obj.tech_factor_ids + obj.ecologic_factor_ids + obj.legal_factor_ids:
                    groups2[each.type_id].append(each)

        custom_pest1 = groups1.values()
        custom_pest2 = groups2.values()

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'time': time,
            'docs': docs,
            'internal_factor': custom_pest1,
            'external_factor': custom_pest2,
            'company': company,
        }
