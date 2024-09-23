import fitz
import io
import logging
import markupsafe
import re

from bs4 import BeautifulSoup
from odoo import api, models
from odoo.tools.pdf import OdooPdfFileReader, OdooPdfFileWriter

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'
    
    def extract_headings_from_binary(self, pdf_binary):
        doc = fitz.open(stream=pdf_binary)
        page_datas = {}
        headers_datas = []
        pattern = r"&lt;(h[1-6])&gt;(.*?)&lt;/\1&gt;"
        for current_page, page in enumerate(doc, 1):
            text_page = page.get_textpage(flags=fitz.TEXT_MEDIABOX_CLIP)
            page_data = text_page.extractHTML()       

            soup = BeautifulSoup(page_data, 'html.parser')
            
            _logger.info(page_data)
            
            h1 = soup.findAll(
                lambda tag:tag.name == "span" and
                '#477da1' in tag["style"])
            h2 = soup.findAll(
                lambda tag:tag.name == "span" and
                '#477da2' in tag["style"])
            h3 = soup.findAll(
                lambda tag:tag.name == "span" and
                '#477da3' in tag["style"])
            h4 = soup.findAll(
                lambda tag:tag.name == "span" and
                '#477da4' in tag["style"])
            h5 = soup.findAll(
                lambda tag:tag.name == "span" and
                '#477da5' in tag["style"])
            h6 = soup.findAll(
                lambda tag:tag.name == "span" and
                '#477da6' in tag["style"])
            
            color_to_h = {
                '#477da1': 'h1',
                '#477da2': 'h2',
                '#477da3': 'h3',
                '#477da4': 'h4',
                '#477da5': 'h5',
                '#477da6': 'h6',
            }
            
            for h in h1 + h2 + h3 + h4 + h5 + h6:
                style = h["style"]
                color = [s.split(":")[1].strip() for s in style.split(";") if "color" in s][0]
                h_tag = color_to_h.get(color)
                h_text = h.text
                
                if h_tag:
                    headers_datas.append((h_tag, h_text, current_page))

        return page_datas, headers_datas
  
    def build_index(self, titles):
        index = []
        stack = [{'level': 0, 'children': index}]

        for tag, title, page in titles:
            level = int(tag[1])
            node = {'title': title, 'page': page, 'children': []}

            while stack and stack[-1]['level'] >= level:
                stack.pop()

            stack[-1]['children'].append(node)

            stack.append({'level': level, 'children': node['children']})

        return index
    
    def generate_html(self, index):
        html = '<ul class="index-list">\n'

        def build_html(index, indent=0):
            nonlocal html
            indent_str = '  ' * indent
            for item in index:
                list_item = (
                    f'<table class="index-line" cellspacing="0" cellpadding="0" style="border: 0px solid #ccc;">'
                    f'  <tr>'
                    f'    <td class="title">{item["title"]}</td>'
                    f'    <td class="dots"></td>'
                    f'    <td class="page-number">{item["page"]}</td>'
                    f'  </tr>'
                    f'</table>'
                )
                html += f'{indent_str}<li class="index-item">{list_item}\n'
                if item['children']:
                    html += f'{indent_str}  <ul class="sub-index-list">\n'
                    build_html(item['children'], indent + 1)
                    html += f'{indent_str}  </ul>\n'
                html += f'{indent_str}</li>\n'

        build_html(index)
        html += '</ul>'
        return html


    def _generate_table_of_contents(self, pdf_binary):
        
        titles = self.extract_headings_from_binary(pdf_binary)[1]
        index = self.build_index(titles)
        html = self.generate_html(index)
                
        return html
    
    def _is_tyt_procedure_edition_report(self, report_ref):
        return self._get_report(report_ref).report_name in ('tyt_process.report_procedure_edition_tyt')
    
    def _calculate_tyt_procedure_edition_report_table_of_contents(self, dpi, fields):
        ''' Calculate table of contents for the report. '''
        
        for field in fields:
            if field['type'] == 'image':
                field['width'] = field['width'] * dpi / 96
                field['height'] = field['height'] * dpi / 96
        

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        # OVERRIDE
        res = super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids)
        if not res_ids:
            return res
        report = self._get_report(report_ref)

        if self._is_tyt_procedure_edition_report(report_ref):
            procedure_editions = self.env[report.model].browse(res_ids)

            streams_to_append = {}
            
            MONTHS = {
                '01': 'Enero',
                '02': 'Febrero',
                '03': 'Marzo',
                '04': 'Abril',
                '05': 'Mayo',
                '06': 'Junio',
                '07': 'Julio',
                '08': 'Agosto',
                '09': 'Septiembre',
                '10': 'Octubre',
                '11': 'Noviembre',
                '12': 'Diciembre',
            }
                
            ABBR_MONTHS = {
                '01': 'Ene',
                '02': 'Feb',
                '03': 'Mar',
                '04': 'Abr',
                '05': 'May',
                '06': 'Jun',
                '07': 'Jul',
                '08': 'Ago',
                '09': 'Sep',
                '10': 'Oct',
                '11': 'Nov',
                '12': 'Dic',
            }
            
            data['months'] = MONTHS
            data['abbr_months'] = ABBR_MONTHS

            cover = self._render_qweb_pdf_prepare_streams(
                        'tyt_process.action_report_procedure_edition_tyt_cover',
                        {
                            **data,
                            'skip_headers': True,
                        },
                        res_ids=procedure_editions.ids,
                    )
            
            meta = self._render_qweb_pdf_prepare_streams(
                        'tyt_process.action_report_procedure_edition_tyt_meta',
                        {
                            **data,
                            'skip_headers': True,
                        },
                        res_ids=procedure_editions.ids,
                    )
            
            body = self._render_qweb_pdf_prepare_streams(
                        'tyt_process.action_report_procedure_edition_tyt_body',
                        {
                            **data,
                            'skip_headers': True,
                        },
                        res_ids=procedure_editions.ids,
                    )
            
            back_cover = self._render_qweb_pdf_prepare_streams(
                        'tyt_process.action_report_procedure_edition_tyt_back_cover',
                        {
                            **data,
                            'skip_headers': True,
                        },
                        res_ids=procedure_editions.ids,
                    )

            for procedure_edition_id, stream in cover.items():
                streams_to_append[procedure_edition_id] = [stream]
                
            for procedure_edition_id, stream in meta.items():
                streams_to_append[procedure_edition_id].append(stream)
            
            toc_dict = {}
            for procedure_edition_id, stream in body.items():
                streams_to_append[procedure_edition_id].append(stream)
                toc_dict[procedure_edition_id] = markupsafe.Markup(self._generate_table_of_contents(stream['stream']))
            
            '''    
            data['toc_dict'] = toc_dict
            
            toc = self._render_qweb_pdf_prepare_streams(
                'tyt_process.action_report_procedure_edition_tyt_toc',
                {
                    **data,
                    'skip_headers': True,
                },
                res_ids=procedure_editions.ids,
            )
            
            for procedure_edition_id, stream in toc.items():
                streams_to_append[procedure_edition_id].append(stream)
            '''
                    
            for procedure_edition_id, stream in back_cover.items():
                streams_to_append[procedure_edition_id].append(stream)

            for procedure_edition_id, additional_stream in streams_to_append.items():
                procedure_edition_stream = res[procedure_edition_id]['stream']
                writer = OdooPdfFileWriter()
                # writer.appendPagesFromReader(OdooPdfFileReader(procedure_edition_stream, strict=False))
                writer.appendPagesFromReader(OdooPdfFileReader(additional_stream[0]['stream'], strict=False))
                writer.appendPagesFromReader(OdooPdfFileReader(additional_stream[1]['stream'], strict=False))
                writer.appendPagesFromReader(OdooPdfFileReader(additional_stream[3]['stream'], strict=False))
                writer.appendPagesFromReader(OdooPdfFileReader(additional_stream[2]['stream'], strict=False))
                writer.appendPagesFromReader(OdooPdfFileReader(additional_stream[4]['stream'], strict=False))
                new_pdf_stream = io.BytesIO()
                writer.write(new_pdf_stream)
                res[procedure_edition_id]['stream'] = new_pdf_stream
                procedure_edition_stream.close()
                additional_stream[0]['stream'].close()
                additional_stream[1]['stream'].close()
                additional_stream[2]['stream'].close()
            
        return res
