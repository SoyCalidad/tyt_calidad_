import base64
import io
import time
from collections import defaultdict
from datetime import datetime, timedelta
# from hola_calidad import HTMLFilter

import pytz
from bs4 import BeautifulSoup
from PIL import Image

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import UserError


class Report_excel_ac(models.AbstractModel):
    _name = 'report.report_excel_ac.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # estilos
        format21_c_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})

        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True})

        format21_gray = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        format21_gray_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, })
        format21_red_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': 'red', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, })
        format26_c_bold = workbook.add_format(
            {'font_size': 26, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True})

        format21_c_bold.set_border()
        format21_left.set_border()
        format21_gray.set_border()
        format21_gray_bold.set_border()
        format26_c_bold.set_border()

        sheet = workbook.add_worksheet('REGISTRO DE ACCIONES',)

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
        sheet.insert_image('B2:B4', "logo.png", {
            'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})

        format21 = workbook.add_format(
            {'font_size': 35, 'align': 'center', 'bold': True})
        format13 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'bold': True})

        # cabecera
        sheet.merge_range(
            'B2:C5', self.env.user.company_id.name, format21_c_bold)
        sheet.merge_range('D2:I5', 'REGISTRO DE ACCIONES', format26_c_bold)
       # sheet.merge_range('G2:J4', 'MOD-' + partners.code,format21_c_bold)
       # sheet.merge_range('G4:J4', 'EDICION -',format21_c_bold)
        date_init = data['form']['date_init'] if data.get(
            'form') and data.get('form').get('date_init') else ''
        date_fin = data['form']['date_fin'] if data.get(
            'form') and data.get('form').get('date_fin') else ''
        sheet.merge_range('J2:J5', 'Fecha inicio: ' +
                          date_init, format21_c_bold)
        sheet.merge_range('K2:K5', 'Fecha fin: ' + date_fin, format21_c_bold)
        sheet.merge_range('B6:F6', 'INFORMACIÓN LA ACCION', format21_c_bold)
        sheet.merge_range('G6:K6', 'SEGUIMIENTO', format21_c_bold)

        # cabecera2
        format13.set_border()
        format21.set_border()

        sheet.set_column(7, 6, 18)
        sheet.set_column(7, 1, 24)
        sheet.set_column(6, 2, 24)
        sheet.set_column(7, 5, 30)
        sheet.set_column(7, 14, 30)
        sheet.set_column(8, 14, 20)
        sheet.set_column(8, 16, 20)
        sheet.set_column(8, 18, 30)
        sheet.set_column(8, 20, 25)
        sheet.set_column(8, 21, 30)
        sheet.merge_range('B7:B8', 'TITULO DE LA ACCIÓN', format21_gray_bold)
        sheet.merge_range('C7:C8', 'TIPO', format21_gray_bold)
        sheet.merge_range('D7:D8', 'ESTADO DE LAS ACCIONES',
                          format21_gray_bold)
        sheet.merge_range('E7:E8', 'FECHA DE CIERRE', format21_gray_bold)
        sheet.merge_range('F7:F8', 'REINCIDENCIA', format21_gray_bold)
        sheet.merge_range('G7:G8', 'FECHA DE SEGUIMIENTO', format21_gray_bold)
        sheet.merge_range(
            'H7:H8', 'RESULTADO DE VERIFICICION ', format21_gray_bold)
        sheet.merge_range('I7:I8', 'EFECTIVIDAD %', format21_gray_bold)
        sheet.merge_range('J7:J8', 'EVIDENCIA DE LA EFICACIA',
                          format21_gray_bold)
        sheet.merge_range('K7:K8', 'IDENTIFICADOR',
                          format21_gray_bold)

        column = 0
        column = column+1
        line = 8

        system_id = data['form']['system_id'] if data['form']['system_id'] else None

        action_nc = self.env['mgmtsystem.action'].search([
            ('date_open', '>=', data['form']['date_init']),
            ('date_open', '<=', data['form']['date_fin']),
            ('system_id', '=', system_id),
        ], order="date_open asc")

        for nc in action_nc:
            actions = dates = types = states = ""
            # altura de celda
            sheet . set_row(line, 30)
            type_action_name = dict(
                nc._fields['type_action'].selection).get(nc.type_action)
            types = types+str(type_action_name)+","
            state_name = dict(nc._fields['state'].selection).get(nc.state)
            states = states+str(state_name)+","
            system_id = nc.system_id.name if nc.system_id else ''
            sheet.write(line, column, nc.name, format21_left)
            sheet.write(line, column+1, types, format21_left)
            sheet.write(line, column+2, states, format21_left)
            sheet.write(line, column+3, str(nc.date_closed), format21_left)
            sheet.write(line, column+4, '', format21_left)
            sheet.write(line, column+5, str(nc.date_deadline), format21_left)
            sheet.write(line, column+6, nc.result, format21_left)
            sheet.write(line, column+7, nc.efficient, format21_left)
            sheet.write(line, column+8, nc.evidence, format21_left)
            sheet.write(line, column+9, system_id, format21_left)
            #sheet.write(line,column+9, '', format21_left)
            #sheet.write(line,column+10, '' , format21_left)
            #sheet.write(line,column+11, '', format21_left)
            #sheet.write(line,column+12, '', format21_left)
            #sheet.write(line,column+13, '', format21_left)

            line = line+1


class NcReport(models.TransientModel):
    _name = "wizard.ac.report"
    _description = "Wizard de reporte de acciones"

    action_ids = fields.Many2many('mgmtsystem.action', string='Acciones')

    system_id = fields.Many2one(
        'mgmtsystem.context.system', string='Identificador', default=lambda self: self.env.ref('hola_calidad.policy_system_1'))

    date_init = fields.Date(
        string='Fecha inicio',
        default=fields.Date.context_today,
        required=True,
    )

    date_fin = fields.Date(
        string='Fecha finalización',
        default=fields.Date.context_today,
        required=True,
    )

    def export_action_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard.ac.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('mgmtsystem_action.report_ac_xlsx').report_action(self, data=datas)


class ActionType(models.Model):
    _name = 'mgmtsystem.action.type'
    _description = 'Tipo de acción'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')


class MgmtsystemAction(models.Model):
    _name = "mgmtsystem.action"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'mgmtsystem.code']
    _description = "Acción"
    _order = "priority desc, sequence, id desc"

    code = fields.Char(string='Código', )

    def _default_company(self):
        return self.env.user.company_id

    def _default_owner(self):
        return self.env.user

    @api.model
    def _elapsed_days(self, open_date, close_date):
        # Get the days between a date object (close_date) and a datetime object (open_datetime)
        # The result is a timedelta object.
        if not open_date or not close_date:
            return 0
        return (close_date - open_date).days
        

    @api.depends('date_open', 'date_closed')
    def _compute_number_of_days_to_open(self):
        for action in self:
            # days_open is the number of days between the date_open field date and the close date
            if action.state == 'done' or action.state == 'close':
                action.number_of_days_to_open = action._elapsed_days(
                    action.date_open.date(), action.date_closed)
            else:
                action.number_of_days_to_open = action._elapsed_days(
                    action.date_open.date(), fields.Date.today())

    @api.depends('date_deadline', 'date_open')
    def _compute_number_of_days_to_close(self):
        for action in self:
            number_of_days_to_close = action._elapsed_days(
                fields.Date.today(), action.date_deadline)
            action.number_of_days_to_close = number_of_days_to_close if number_of_days_to_close > 0 else 0

    @api.depends('date_deadline', 'date_closed')
    def _compute_number_of_days_of_ret(self):
        for action in self:
            if action.state == 'done' or action.state == 'close':
                number_of_days_of_ret = action._elapsed_days(
                    action.date_deadline, action.date_closed)
            else:
                number_of_days_of_ret = action._elapsed_days(
                    action.date_deadline, fields.Date.today())

            action.number_of_days_of_ret = number_of_days_of_ret if number_of_days_of_ret > 0 else 0

    name = fields.Char('Nombre', required=True)
    active = fields.Boolean('Activo', default=True)

    priority = fields.Selection(
        [
            ('0', 'Baja'),
            ('1', 'Normal'),
            ('2', 'Alta'),
            ('3', 'Muy alta'),
        ],
        default='0',
        index=True,
        string="Prioridad"
    )

    sequence = fields.Integer(
        'Secuencia',
        index=True,
        default=10,
        help="Da la secuencia a las acciones y como se van a ver en lista."
    )

    process_id = fields.Many2one('mgmt.categ', string='Proceso')
    system_id = fields.Many2one(
        'mgmtsystem.context.system', string='Identificador', default=lambda self: self.env.ref('hola_calidad.policy_system_1'))

    date_deadline = fields.Date('Fecha límite')

    date_open = fields.Datetime(
        'Fecha de apertura',
        default=fields.Date.context_today,
    )

    date_closed = fields.Date('Fecha de cierre', store=True)

    number_of_days_to_open = fields.Integer(
        '# de días abierto',
        compute=_compute_number_of_days_to_open,
    )
    number_of_days_to_close = fields.Integer(
        '# de días para cerrar',
        compute=_compute_number_of_days_to_close,
    )

    number_of_days_of_ret = fields.Integer(
        '# de días de retraso',
        compute=_compute_number_of_days_of_ret,
    )
    reference = fields.Char(
        'Referencia',
        required=True,
        default=lambda self: _('New')
    )

    user_id = fields.Many2one(
        'res.users',
        'Responsable de ejecución',
        default=_default_owner,
        required=True,
    )

    track_user_id = fields.Many2one(
        'hr.employee', string='Responsable de seguimiento')

    description = fields.Html('Descripción')

    date_follow = fields.Date(
        string='Fecha de seguimiento',
    )
    result = fields.Text('Resultado de verificación')
    efficient = fields.Integer(
        string='Efectividad',
    )
    evidence = fields.Binary(
        string='Evidencia',
    )

    type_action = fields.Selection([
        ('immediate', 'Immediate Action'),
        ('correction', 'Corrective Action'),
        ('prevention', 'Preventive Action'),
        ('improvement', 'Improvement Opportunity')
    ], 'Response Type')

    type_action_id = fields.Many2one(
        'mgmtsystem.action.type', string='Tipo', required=True)

    company_id = fields.Many2one(
        'res.company',
        'Compañia',
        default=_default_company,
    )

    state = fields.Selection(
        string=u'Estado',
        selection=[('open', 'Abierto'),
                   ('follow', 'En seguimiento'),
                   ('done', 'Cerrado'),
                   ('cancel', 'Cancelado')],
        default='open',
        group_expand='_group_expand_states',
    )

    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    resources = fields.Text(string='Recursos')

    def send_follow(self):
        self.write({'state': 'follow'})

    def send_done(self):
        self.write({'state': 'done'})

    def send_cancel(self):
        self.write({'state': 'cancel'})

    @api.constrains('state')
    def _check_state(self):
        for record in self:
            if record.state == 'done':
                record.write({'date_closed': fields.Datetime.now(self)})

    """
    @api.model
    def send_mail_for_action(self, action, force_send=True):
        template = self.env.ref(
            'mgmtsystem_action.email_template_new_action_reminder')
        template.send_mail(action.id, force_send=force_send)
        return True

    def get_action_url(self):
        #Return action url to be used in email templates.
        base_url = self.env['ir.config_parameter'].get_param(
            'web.base.url',
            default='http://localhost:8069'
        )
        url = ('{}/web#db={}&id={}&model={}').format(
            base_url,
            self.env.cr.dbname,
            self.id,
            self._name
        )
        return url
    """

    def case_open(self):
        """ Opens case """
        for case in self:
            case.write({
                'active': True,
                'state': 'open'})
        return True
