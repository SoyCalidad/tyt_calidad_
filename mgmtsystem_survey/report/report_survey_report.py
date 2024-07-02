from odoo import api, fields, models
from odoo.http import request

from collections import defaultdict
from math import ceil
import base64
import io
from PIL import Image


class SurveyReport(models.AbstractModel):
    _name = 'report.mgmtsystem_survey.survey_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Resultados de encuesta' # before: _description = 'Análisis de encuesta'

    def generate_xlsx_report(self, workbook, data, partners):
        """Generate a xls report with the data
        """

        format_title = workbook.add_format(
            {'font_size': 13, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'align': 'center'})
        format_header = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 1, 'bg_color': '#EEEEEE'})
        format_1 = workbook.add_format(
            {'font_size': 10, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'bold': True, 'text_wrap': True, 'border': 1, 'bg_color': '#A0A0A0'})
        format_2 = workbook.add_format(
            {'font_size': 9, 'font_name': 'Arial', 'valign': 'vcenter', 'text_wrap': True, 'border': 1, 'align': 'center', })
        format_data = workbook.add_format(
            {'font_size': 11, 'font_name': 'Arial', 'valign': 'vcenter', 'align': 'center', 'border': True})


        '''
        sheet = workbook.add_worksheet('Resultados')
        sheet.merge_range('A1:A3', '', format_data)
        sheet.merge_range('B1:C1', 'ANÁLISIS DE LA ENCUESTA', format_title)
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 2, 20)
        sheet.set_column(3, 4, 15)

        model_id = self.env['ir.model'].search(
            [('model', '=', 'report.mgmtsystem_survey.survey_report')],)
        code = self.env['documentary.control'].search(
            [('model_id', '=', model_id.id)], limit=1)

        buf_image = io.BytesIO(base64.b64decode(self.env.company.logo))
        im = Image.open(buf_image)
        width, height = im.size
        image_width = width
        image_height = height
        cell_width = 128.0
        cell_height = 40.0
        x_scale = cell_width/image_width
        y_scale = cell_height/image_height
        sheet.insert_image('A1', "any_name.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})

        code = code.code if code and code.code else ''
        version = str(partners.version) or ''
        date_validate = partners.date_validate.strftime(
            '%d/%m/%Y') if partners.date_validate else ''

        sheet.merge_range(1, 1, 2, 2, partners.title, format_title)
        sheet.write(0, 3, 'Código:', format_header)
        sheet.write(1, 3, 'Versión:', format_header)
        sheet.write(2, 3, 'Fecha de aprobación:', format_header)
        sheet.write(0, 4, code, format_2)
        sheet.write(1, 4, version, format_2)
        sheet.write(2, 4, date_validate, format_2)

        entrie_row = 4

        Survey = request.env['survey.survey']
        survey = partners
        '''


        '''
        question_list = []
        if survey.page_ids:
            for page in survey.page_ids:
                for question in page.question_ids:
                    question_dict = {
                        'question': question,
                        'input_summary': Survey.get_input_summary(question),
                        'prepare_result': Survey.prepare_result(question),
                    }
                    question_list.append(question_dict)
        else:
            for question in survey.question_ids:
                question_dict = {
                    'question': question,
                    'input_summary': Survey.get_input_summary(question),
                    'prepare_result': Survey.prepare_result(question),
                }
                question_list.append(question_dict)
        index = 0
        for each in question_list:
            if type(each['prepare_result']) is dict:
                question = each['question']
                if len(question.question) >= 40:
                    row_height = ceil(len(question.question)/40)*12
                    sheet.set_row(entrie_row, row_height)
                sheet.write(entrie_row, 0,
                            each['question'].question, format_header)
                sheet.write(entrie_row, 1, 'Cantidad', format_header)
                sheet.write(entrie_row, 2, 'Porcentaje', format_header)
                entrie_row += 1
                if each['prepare_result'].get('answers'):
                    total_sum = 0
                    for x in each['prepare_result']['answers']:
                        if type(x) is dict and x.get('count'):
                            total_sum += x['count']
                    #  = sum([x['count']
                    #                 for x in each['prepare_result']['answers']])
                    for ans in each['prepare_result']['answers']:
                        sheet.write_string(entrie_row, 0, str(ans['text']) if type(
                            ans) != int else str(ans), format_2)
                        sheet.write(entrie_row, 1, ans['count'] if type(
                            ans) != int and ans.get('count') else '', format_2)
                        sheet.write(entrie_row, 2, str(
                            round(ans['count']*100/total_sum, 2)) + ' %' if total_sum > 0 else 0, format_2)
                        entrie_row += 1
                    chart = workbook.add_chart({'type': 'pie'})
                    chart.add_series({
                        # "=Resultados!$A$%s:$A$%s" % (str(entrie_row+1-len(each['prepare_result']['answers'])), str(entrie_row)),
                        'categories':  ['Resultados', entrie_row-len(each['prepare_result']['answers']), 0, entrie_row-1, 0],
                        'values':     '=Resultados!$B$%s:$B$%s' % (str(entrie_row+1-len(each['prepare_result']['answers'])), str(entrie_row)),
                        'points': [
                            {'fill': {'color': 'green'}},
                            {'fill': {'color': 'red'}},
                        ],
                    })

                    chart.set_title({
                        'name':    each['question'].question,
                        'name_font': {
                            'name': 'Calibri',
                            'color': 'black',
                            'size': 10,
                        },
                    })
                    chart.set_size({'width': 300, 'height': 200})
                    sheet.insert_chart('E%s' % str(5+index), chart)
                    index += 10
                else:
                    total_sum = 0

                # Graph

            else:
                sheet.merge_range(entrie_row, 0, entrie_row,
                                  2, each['question'].question, format_header)
                entrie_row += 1
                for ans in each['prepare_result']:
                    for a in ans:
                        text = a.value_text or a.value_number or a.value_date or a.value_free_text
                        if a.value_date:
                            text = text.strftime('%d/%m/%Y')
                        sheet.merge_range(
                            entrie_row, 0, entrie_row, 2, text, format_2)
                    # sheet.write(entrie_row, 3, ans['count'])
                    entrie_row += 1
            entrie_row += 1

        '''

        sheet = workbook.add_worksheet('Respuestas') # before: sheet2 = workbook.add_worksheet('Respuestas')

        max_len = 0

        question_position = {
            'Fecha': 0,
        }
        sheet.write(0, 0, 'Fecha', format_header)
        sheet.set_column(0, 0, 20)
        i = 1
        for question in partners.question_ids:
            if question.question_type == 'matrix':
                for label in question.matrix_row_ids:  #before: for label in question.labels_ids_2:
                    title = label.value
                    question_position[title] = i
                    sheet.write(0, i, title, format_header)
                    
                    max_len = max(max_len, len(title))
                    sheet.set_column(i, i, 40)
                    i += 1
            else:
                title = question.title
                question_position[title] = i
                sheet.write(0, i, title, format_header)
                max_len = max(max_len, len(title))
                sheet.set_column(i, i, 40)
                i += 1

            # Height format
            

        height = ceil(max_len/40)*12
        sheet.set_row(0, height)

    
        entrie_row = 1
        max_len = 12
        for input in partners.user_input_ids:
            suggested = ''
            answer_values = {}
            max_n = 1
            has_lists = False
            for answer in input.user_input_line_ids:
                text = answer.value_char_box or answer.value_numerical_box or answer.value_text_box or '' # before: text = answer.value_text or answer.value_number or answer.value_free_text or ''
                suggested = answer.suggested_answer_id.value + \
                    '\n' if answer.suggested_answer_id else ''
                date = answer.value_date or ''
                if date:
                    date = date.strftime('%d/%m/%Y')
                value = text + date + suggested
                if answer.question_id.question_type == 'matrix':
                    title = answer.matrix_row_id.value if answer.matrix_row_id else '' # before: 
                else:
                    title = answer.question_id.title
                if answer_values.get(title) and not type(answer_values[title]) is list:
                    answer_values[title] = [answer_values[title], value]
                    has_lists = True
                    max_n = max(max_n, len(answer_values[title]))
                elif answer_values.get(title) and type(answer_values[title]) is list:
                    answer_values[title].append(value)
                    max_n = max(max_n, len(answer_values[title]))
                else:
                    answer_values[title] = value if not answer_values.get(
                        title) else ''
                
            if answer_values:
                answer_values['Fecha'] = input.create_date.strftime('%d/%m/%Y')
                for key, value in answer_values.items():
                    if key:
                        if has_lists:
                            current_row = entrie_row
                            if type(value) == list:
                                for v in value:
                                    sheet.write(current_row, question_position[key], v, format_2)
                                    current_row += 1
                            else:
                                sheet.merge_range(entrie_row, question_position[key], entrie_row+max_n-1, question_position[key], value, format_2)
                        else:
                            sheet.write(
                                entrie_row, question_position[key], value, format_2)
                        # Height format
                        if value:
                            len_value = 40*(value.count('\n') + 1) - len(value)
                            max_len = max(max_len, len_value)
                entrie_row += max_n
                height = ceil(max_len/40)*12
                sheet.set_row(entrie_row, height)
            

        workbook.close()
