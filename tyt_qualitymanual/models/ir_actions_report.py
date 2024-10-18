# -*- coding: utf-8 -*-
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

    def _is_tyt_quality_manual_report(self, report_ref):
        return self._get_report(report_ref).report_name in ('tyt_qualitymanual.mgmtsystem_qualitymanual_tyt_report')

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        res = super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids)
        if not res_ids:
            return res
        report = self._get_report(report_ref)

        if self._is_tyt_quality_manual_report(report_ref):
            quality_manuals = self.env[report.model].browse(res_ids)

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
                'tyt_qualitymanual.mgmtsystem_qualitymanual_tyt_cover_report_action',
                {
                    **data,
                    'skip_headers': True,
                },
                res_ids=quality_manuals.ids,
            )

            body = self._render_qweb_pdf_prepare_streams(
                'tyt_qualitymanual.mgmtsystem_qualitymanual_tyt_body_report_action',
                {
                    **data,
                    'skip_headers': True,
                },
                res_ids=quality_manuals.ids,
            )

            back_cover = self._render_qweb_pdf_prepare_streams(
                'tyt_qualitymanual.mgmtsystem_qualitymanual_tyt_back_cover_report_action',
                {
                    **data,
                    'skip_headers': True,
                },
                res_ids=quality_manuals.ids,
            )

            for quality_manual_id, stream in cover.items():
                streams_to_append[quality_manual_id] = [stream]

            toc_dict = {}
            for quality_manual_id, stream in body.items():
                streams_to_append[quality_manual_id].append(stream)
                toc_dict[quality_manual_id] = markupsafe.Markup(self._generate_table_of_contents(stream['stream']))

            data['toc_dict'] = toc_dict

            toc = self._render_qweb_pdf_prepare_streams(
                'tyt_qualitymanual.mgmtsystem_qualitymanual_tyt_toc_report_action',
                {
                    **data,
                    'skip_headers': True,
                },
                res_ids=quality_manuals.ids,
            )

            for quality_manual_id, stream in toc.items():
                streams_to_append[quality_manual_id].append(stream)

            for quality_manual_id, stream in back_cover.items():
                streams_to_append[quality_manual_id].append(stream)

            for quality_manual_id, additional_stream in streams_to_append.items():
                quality_manual_stream = res[quality_manual_id]['stream']
                writer = OdooPdfFileWriter()
                writer.appendPagesFromReader(OdooPdfFileReader(additional_stream[0]['stream'], strict=False))
                writer.appendPagesFromReader(OdooPdfFileReader(additional_stream[2]['stream'], strict=False))
                writer.appendPagesFromReader(OdooPdfFileReader(additional_stream[1]['stream'], strict=False))
                writer.appendPagesFromReader(OdooPdfFileReader(additional_stream[3]['stream'], strict=False))
                new_pdf_stream = io.BytesIO()
                writer.write(new_pdf_stream)
                res[quality_manual_id]['stream'] = new_pdf_stream
                quality_manual_stream.close()
                additional_stream[0]['stream'].close()
                additional_stream[1]['stream'].close()
                additional_stream[2]['stream'].close()

        return res
