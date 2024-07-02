# -*- coding: utf-8 -*-
import base64
import io
import os
import time
from datetime import datetime

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class PorterForcesReportPDF(models.AbstractModel):
    _name = 'report.mgmtsystem_context.report_porter_forces_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        external_issue = self.env['mgmtsystem.context.external_issue'].browse(
            data['external_issue'])
        return {
            'docs': external_issue,
            'doc_ids': self.ids,
            'time': time,
        }


class PorterForcesReportXLS(models.AbstractModel):
    _name = 'report.mgmtsystem_context.report_porter_forces'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        """Generate a xls report with the data

        Arguments:
            workbook {object} -- A object that represents a Excel workbook
            data {dict} -- The data of the report
            partners {object} -- A class object

        Raises:
            UserError: When the user choose a initial balance but no a initial date
        """

        format_title = workbook.add_format(
            {'font_size': 13, 'font_name': 'Arial', 'valign': 'vcenter', 'bold': True, 'align': 'center'})

        sheet = workbook.add_worksheet('Fuerzas de Porter')

        sheet.merge_range(0, 0, 1, 4, 'DIAGRAMA DE PORTER', format_title)
        if data and data.get('is_wizard'):
            external_issue = self.env['mgmtsystem.context.external_issue'].browse(
                data['external_issue'])
            ut = external_issue.forces
        else:
            external_issue = partners.external_issue_id
            ut = external_issue.forces

        sheet.insert_textbox('E4', ut[2].context_force.name + '\n' + ut[2].description,
                             {'x_offset': 10,
                              'y_offset': 10,
                              'width': 200,
                              'height': 100,
                              'align': {'vertical': 'middle',
                                        'horizontal': 'center'
                                        },
                              'gradient': {'colors': ['#D6EBCF',
                                                      '#9CB86E',
                                                      '#156B13']
                                           },
                              })

        sheet.insert_textbox('A11', ut[1].context_force.name + '\n' + ut[1].description,
                             {'x_offset': 10,
                              'y_offset': 10,
                              'width': 200,
                              'height': 100,
                              'align': {'vertical': 'middle',
                                        'horizontal': 'center'
                                        },
                              'gradient': {'colors': ['#D6EBCF',
                                                      '#9CB86E',
                                                      '#156B13']
                                           },
                              })

        sheet.insert_textbox('E11', ut[3].context_force.name + '\n' + ut[3].description,
                             {'x_offset': 10,
                              'y_offset': 10,
                              'width': 200,
                              'height': 100,
                              'align': {'vertical': 'middle',
                                        'horizontal': 'center'
                                        },
                              'gradient': {'colors': ['#D6EBCF',
                                                      '#9CB86E',
                                                      '#156B13']
                                           },
                              })

        sheet.insert_textbox('I11', ut[0].context_force.name + '\n' + ut[0].description,
                             {'x_offset': 10,
                              'y_offset': 10,
                              'width': 200,
                              'height': 100,
                              'align': {'vertical': 'middle',
                                        'horizontal': 'center'
                                        },
                              'gradient': {'colors': ['#D6EBCF',
                                                      '#9CB86E',
                                                      '#156B13']
                                           },
                              })

        sheet.insert_textbox('E18', ut[4].context_force.name + '\n' + ut[4].description,
                             {'x_offset': 10,
                              'y_offset': 10,
                              'width': 200,
                              'height': 100,
                              'align': {'vertical': 'middle',
                                        'horizontal': 'center'
                                        },
                              'gradient': {'colors': ['#D6EBCF',
                                                      '#9CB86E',
                                                      '#156B13']
                                           },
                              })

        workbook.close()
