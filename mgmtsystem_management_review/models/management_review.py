# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import logging
import datetime

_logger = logging.getLogger(__name__)


class ManagementReviewTeam(models.Model):
    _name = "management.review.team"
    _description = "Comité de calidad"

    name = fields.Char(
        string='Nombre',
        required=True,
    )
    line_ids = fields.Many2many(
        string='Integrantes',
        comodel_name='management.review.team.line',
        relation='management_review_team_line_management_review_team',
        column1='line_id',
        column2='management_review_team_id',
    )


class ManagementReviewTeamLine(models.Model):
    _name = "management.review.team.line"
    _description = "Integrante comité de calidad"

    employee_id = fields.Many2one(
        string='Empleado',
        required=True,
        comodel_name='hr.employee',
        ondelete='cascade',
    )
    job_id = fields.Many2one(
        string='Puesto',
        comodel_name='hr.job',
        related='employee_id.job_id'
    )
    qlty_job_id = fields.Many2one(
        string='Puesto en el comité',
        comodel_name='review.team.job',
        ondelete='cascade',
    )
    puesto_comité = fields.Text(string='Puesto en el comité')
    description = fields.Text(
        string='Descripción',
    )


class ManagementReviewTeamLineJob(models.Model):
    _name = 'review.team.job'
    _description = 'Puesto en el comité de calidad'

    name = fields.Binary(string='Nombre')
    description = fields.Text(string='Descripción')


class ReviewPlan(models.Model):
    _name = 'management.review.plan'
    _inherit = 'mgmtsystem.validation.mail'
    _description = "Programa de revisiones"

    name = fields.Char(
        string=u'Nombre',
        required=True,
        default="Programa de revisiones"
    )

    numero = fields.Char(
        string="Numero de secuencia",
        readonly=True,
        required=True,
        copy=False,
        default='Sin definir'
    )

    edition_id = fields.Many2one(
        string=u'Procedimiento',
        comodel_name='process.edition',
        domain="[('state', '=', 'validate_ok'), ('active', '=', True)]",
        ondelete='cascade',
    )

    line_ids = fields.One2many(
        string='Revisiones',
        comodel_name='management.review',
        inverse_name='plan_id',
    )

    def create_action(self, vuser_id):
        action = self.env.ref('hola_calidad.p_mail_activity_action').read()[0]
        self.env.cr.execute("""SELECT id FROM ir_model 
        WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
            action['context'] = {
                'default_res_id': self.ids[0],
                'default_res_model': self._name,
                'default_res_model_id': model_id,
                'default_user_id': vuser_id,
            }
        return action

    def action_show_revisiones(self):
        type_action = self._context.get('type_action', '')
        if type_action == '':
            return
        ids = []

        if type_action == 'action':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_opp_action_action').read()[0]
            ids = self.opp_ids.ids
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain

        elif type_action == 'nc':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_risk_action_action').read()[0]
            ids = self.risk_ids.ids
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain

        elif type_action == 'target':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_risk_action_action').read()[0]
            ids = self.risk_ids.ids
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain

        elif type_action == 'revi':
            action_rec = self.env.ref(
                'mgmtsystem_management_review.action_management_review').read()[0]
            ids = self.line_ids.ids
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain

        return action_rec

    def action_reset_all_aproval(self):
        for line in self.line_ids:
            line.aproval = True


class ManagementReview(models.Model):
    _name = 'management.review'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Revisión por la dirección'

    name = fields.Char(
        string='Nombre',
        required=True,
    )

    plan_id = fields.Many2one(
        string='Plan de revisiones',
        comodel_name='management.review.plan',
        ondelete='cascade',
    )

    aproval = fields.Boolean(u'Aprobada')

    managementreview_id = fields.Many2one(
        string='Revisión anterior',
        comodel_name='management.review',
        ondelete='cascade',
    )

    record_meeting_ids = fields.Many2many(
        'record.meeting', string='Actas de reunión')

    record_meeting_actions = fields.Html(
        compute='_compute_record_meeting_actions', string='Acciones de actas de reunión')

    record_meeting_interpretation = fields.Text(
        'Interpretación de actas de reunión')

    @api.depends('record_meeting_ids')
    def _compute_record_meeting_actions(self):
        for record in self:
            table = '''<div style="margin-bottom:20px;"><table class="table table-bordered">'''
            table += '''<thead><tr><th>Referencia</th><th>Título</th><th>Tipo</th><th>Responsable de ejecución</th><th>Estado</th></tr></thead>'''
            table += '''<tbody>'''
            for record_meeting in record.record_meeting_ids:
                table += '''<tr><td colspan="5">{}</td></tr>'''.format(
                    record_meeting.name)
                for line in record_meeting.line_ids:
                    for action in line.action_ids:
                        state = dict(action._fields['state'].selection).get(
                            action.state)
                        table += '''<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'''.format(
                            action.reference, action.name, action.type_action_id.name, action.user_id.name, state)
            table += '''</tbody></table><div>'''
            record.record_meeting_actions = table

    meetings_count = fields.Integer(
        string='# de actas de reunión',
        default=0,
        compute='_compute_meetings_count'
    )

    def create_action(self, vuser_id):
        action = self.env.ref('hola_calidad.p_mail_activity_action').read()[0]
        self.env.cr.execute("""SELECT id FROM ir_model 
                          WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        action['context'] = {
            'default_res_id': self.ids[0],
            'default_res_model': self._name,
            'default_res_model_id': model_id,
            'default_user_id': vuser_id,
        }
        return action

    @api.depends('record_meeting_ids')
    def _compute_meetings_count(self):
        for record in self:
            record.meetings_count = len(record.record_meeting_ids)

    def action_show_meetings(self):
        action = self.env.ref(
            'mgmtsystem_comunication.record_meeting_action').read()[0]
        ids = self.record_meeting_ids.ids
        domain = [('id', 'in', ids)]
        action['domain'] = domain
        return action
        
    date_management_review = fields.Date(
        string='Fecha de revisión',
        default=fields.Date.context_today,
    )
    is_last = fields.Boolean(
        string='Solo el último registro',
        default=False,
    )
    # Si quiere solo el ultimo o todas las versiones, seleccionable/boolean

    date_ini = fields.Date(
        string='Fecha de inicio',
        default=fields.Date.context_today,
        required=True,
    )
    date_fin = fields.Date(
        string='Fecha de fin',
        default=fields.Date.context_today,
        required=True,
    )

    introduction = fields.Text(
        string='Introducción',
    )

    team_id = fields.Many2one(
        string='Comité',
        comodel_name='soycalidad.comittee',
        ondelete='cascade',
    )

    foda = fields.Html(
        string='FODA',
        readonly=True,
        store=True,
    )
    foda_description = fields.Text(
        string='Interpretación',
    )

    def generate_foda(self):
        if self.is_last:
            swot_ids = self.env['mgmtsystem.context.swot'].search(
                ['&', ('date_validate', '>=', self.date_ini), ('date_validate', '<=', self.date_fin)], order='date_validate desc', limit=1)
        else:
            swot_ids = self.env['mgmtsystem.context.swot'].search(
                ['&', ('date_validate', '>=', self.date_ini), ('date_validate', '<=', self.date_fin)], order='date_validate asc')
        foda_tmp = ""
        for swot in swot_ids:
            foda_tmp = foda_tmp + "<div style='margin-bottom:20px;'><table class='table table-bordered'>"
            link = ("<a data-oe-id=%s data-oe-model='mgmtsystem.context.swot' href=#id=%s&model=mgmtsystem.context.swot>%s</a>") % (
                swot.id, swot.id, swot.name)
            foda_tmp = foda_tmp + "<tr><td colspan='2'>"+link + \
                "</td></tr><tr><td width='50%'><strong>Fortalezas</strong></td><td width='50%'><strong>Oportunidades</strong></td></tr><tr><td><ul>"
            foda_tmp = foda_tmp + ("<li>%s</li>") % ('</li><li>'.join(
                x.name for x in swot.fortalezas)) + "</ul></td><td><ul>"
            foda_tmp = foda_tmp + ("<li>%s</li>") % ('</li><li>'.join(x.name for x in swot.oportunidades)) + \
                "</ul></td></tr><tr><td><strong>Debilidades</strong></td><td><strong>Amenazas</strong></td></tr><tr><td><ul>"
            foda_tmp = foda_tmp + ("<li>%s</li>") % ('</li><li>'.join(
                x.name for x in swot.debilidades)) + "</ul></td><td><ul>"
            foda_tmp = foda_tmp + ("<li>%s</li>") % ('</li><li>'.join(
                x.name for x in swot.amenazas)) + "</ul></td></tr></table></div>"
        return foda_tmp

    stakeholders_id = fields.Many2one(
        'mgmtsystem.stakeholders', string='Partes interesadas')
    stakeholders_description = fields.Text(string='Interpretación')

    suppliers_info = fields.Html(
        string='Calificación de proveedores',
        readonly=True,
        store=True,
    )
    suppliers_description = fields.Text(
        string='Interpretación',
    )

    def generate_suppliers(self):
        supplier_table = '''<div style="margin-bottom:20px;"><table class="table table-bordered">{}{}</table></div>'''
        suppliers_header = '''<tr><th>Proveedor</th><th>Calificación</th><th>Fecha de calificación</th></tr>'''
        suppliers_row_title = '''<tr><td colspan="3"><strong>{}</strong></td></tr>'''
        suppliers_row = '''<tr><td>{}</td><td>{}</td><td>{}</td></tr>'''
        rows_content = ''''''
        suppliers = self.env['res.partner'].search([('supplier', '=', True)])
        date_ini_time = datetime.datetime.combine(
            self.date_ini, datetime.time.min)
        date_fin_time = datetime.datetime.combine(
            self.date_fin, datetime.time.max)
        for supplier in suppliers:
            if self.is_last:
                evaluation_history_id = self.env['res.partner.evaluation.history'].search([('partner_id', '=', supplier.id), (
                    'date_history', '>=', date_ini_time), ('date_history', '<=', date_fin_time)], order='date_history desc', limit=1)
                if evaluation_history_id:
                    rows_content += suppliers_row_title.format(supplier.name)
                    link = ("<a data-oe-id=%s data-oe-model='res.partner.evaluation.history' href=#id=%s&model=res.partner.evaluation.history>%s</a>") % (
                        evaluation_history_id.id, evaluation_history_id.id, evaluation_history_id.evaluation_id.name)
                    date_history = evaluation_history_id.date_history.strftime(
                        '%d/%m/%Y %H:%M') if evaluation_history_id.date_history else ''
                    rows_content += suppliers_row.format(
                        link, evaluation_history_id.qualification, date_history)
            else:
                evaluation_history_ids = self.env['res.partner.evaluation.history'].search([('partner_id', '=', supplier.id), (
                    'date_history', '>=', date_ini_time), ('date_history', '<=', date_fin_time)], order='date_history asc')
                if evaluation_history_ids:
                    rows_content += suppliers_row_title.format(supplier.name)
                    for evaluation in evaluation_history_ids:
                        link = ("<a data-oe-id=%s data-oe-model='res.partner.evaluation.history' href=#id=%s&model=res.partner.evaluation.history>%s</a>") % (
                            evaluation.id, evaluation.id, evaluation.evaluation_id.name)
                        date_history = evaluation.date_history.strftime(
                            '%d/%m/%Y %H:%M')
                        rows_content += suppliers_row.format(
                            link, evaluation.qualification, date_history)

        return supplier_table.format(suppliers_header, rows_content)

    process = fields.Html(
        string='Procesos',
        readonly=True,
        store=True,
    )
    process_description = fields.Text(
        string='Interpretación',
    )

    def generate_process(self):
        process = self.env['mgmt.process'].search(
            [('create_date', '>=', self.date_ini), ('create_date', '<=', self.date_fin), ('active', '=', True)])
        pr_temp = ''
        pr_temp += "<div style='margin-bottom:20px;'><table class='table table-bordered'><tr style='align=center'><th>Código</th><th>Nombre</th><th>Edición</th></tr>"
        for p in process:
            code = p.code if p.code else ''
            last_edition = p.last_edition if p.last_edition else ''
            link = ("<a data-oe-id=%s data-oe-model='mgmt.process' href=#id=%s&model=mgmt.process>%s</a>") % (
                p.id, p.id, p.name)
            pr_temp += "<tr><td>" + code + "</td><td>" + link + \
                "</td><td>" + last_edition + "</td></tr>"
        pr_temp += "</table></div>"
        return pr_temp

    target = fields.Html(
        string='Objetivos',
        readonly=True,
        store=True,
    )
    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    target_description = fields.Text(
        string='Interpretación',
    )

    def generate_target(self):
        target_ids = self.env['mgmtsystem.target'].search(
            [('state', '=', 'active')], order='source, process_id')
        data_tmp = "<div style='margin-bottom:20px;'><table class='table table-bordered' style='max-width=100px'>"
        target_table = ("%s<tr><th>%s</th><th>%s</th><th>%s</th></tr>") % (
            data_tmp, "Código", "Nombre", "Descripción")
        data_tmp = data_tmp + "<tr><td><strong>Perspectiva</strong></td><td><strong>Objetivo</strong></td><td><strong>Procedimiento</strong></td><td><strong>Indicador</strong></td><td><strong>Meta</strong></td><td><strong>Frecuencia</strong></td><td><strong>Mediciones</strong></td></tr>"
        for data in target_ids:
            target_table = ("%s<tr><td>%s</td><td>%s</td><td>%s</td></tr>") % (
                target_table, data.code, data.name, data.description)
            link = ("<a data-oe-id=%s data-oe-model='mgmtsystem.target' href=#id=%s&model=mgmtsystem.target>%s</a>") % (
                data.id, data.id, str(data.code)+"<br></br>"+str(data.name))
            len_indicator = str(len(data.indicator_ids))
            source = dict(data._fields['source'].selection).get(data.source)
            data_tmp = data_tmp + "<tr><td rowspan='"+len_indicator+"'>"+source+"</td><td rowspan='" + \
                len_indicator+"'>"+link+"</td><td rowspan='" + \
                len_indicator+"'>"+data.process_id.name+"</td>"

            i = data.indicator_ids[len(
                data.indicator_ids)-1] if data.indicator_ids else False
            if i:
                data_tmp = data_tmp + ("<td>%s</td><td>%s</td><td>%s</td>") % (
                    i.name, i.goal_id.name, i.measurement_frequency.name)
                x = i.history_ids[len(i.history_ids) -
                                  1] if i.history_ids else False
                if x:
                    data_tmp = data_tmp + "<td>" + \
                        str(x.date) + ' | ' + str(x.expected_result) + \
                        " → "+str(x.real_result) + "</td></tr><tr>"

            data_tmp = data_tmp + "</tr>"
        data_tmp = data_tmp + "</table></div>"
        return data_tmp

    def action_view_graph_indicator(self):
        action_rec = self.env.ref(
            'mgmtsystem_target.indicator_action_2').read()[0]
        action_rec['views'] = [
            (self.env.ref('mgmtsystem_target.indicator_view_graph').id, 'graph')]
        action_rec['context'] = dict(self.env.context)
        return action_rec

    survey_ids = fields.Many2many(
        string='Encuestas',
        comodel_name='survey.survey',
        relation='survey_management_review',
        column1='survey_id',
        column2='managementreview_id',
    )
    survey_description = fields.Text(
        string='Interpretación de encuestas')

    nonconformity_action = fields.Text(
        string='No conformidades y acciones',
    )
    nonconformity_action_description = fields.Text(
        string='Interpretación',
    )

    def generate_nonconformity_action(self):
        nonconformities = self.env['mgmtsystem.nonconformity'].search(
            ['&', ('date_found', '>=', self.date_ini), ('date_found', '<=', self.date_fin)], order='date_found asc')
        actions = self.env['mgmtsystem.action'].search(
            ['&', ('date_open', '>=', self.date_ini), ('date_open', '<=', self.date_fin)], order='date_open asc')
        actions_correction = actions.search(
            [('type_action', '=', 'correction')])
        actions_prevention = actions.search(
            [('type_action', '=', 'prevention')])
        data_tmp = "En el rango de tiempo evaluado, se originaron:\nNo conformidades: "+str(len(nonconformities))+"\nAcciones correctivas: "+str(
            len(actions_correction))+"\nAcciones preventivas: "+str(len(actions_prevention))
        return data_tmp

    audit = fields.Html(
        string='Auditorías',
        readonly=True,
        store=True,
    )
    audit_description = fields.Text(
        string='Interpretación',
    )

    def generate_audit(self):
        data_tmp = "<div style='margin-bottom:20px;'><table class='table table-bordered'>"
        data_tmp += '''<tr><th colspan="3"><strong>Nombre</strong></th>
                    <th colspan="2"><strong>Auditor</strong></th></tr>'''
        line_row = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'
        if self.is_last:
            audit_ids = self.env['audit.report'].search(
                [('audit_id.date_init', '>=', self.date_ini)], order='id desc', limit=1)
        else:
            audit_ids = self.env['audit.report'].search(
                [('audit_id.date_init', '>=', self.date_ini)], order='id asc')
        for data in audit_ids:
            name = ("<a data-oe-id=%s data-oe-model='audit.report' href=#id=%s&model=audit.report>%s</a>") % (
                data.id, data.id, data.name)
            auditor_name = data.auditor_id.name if data.auditor_id else ''  
            data_tmp += "<tr><td colspan='2'>"+name+"</td><td colspan='2'>" + \
                auditor_name+"</td></tr>"
            if data.line_ids:
                data_tmp += '''<tr><th><strong>Proceso</strong></th>
                    <th><strong>Tipo de hallazgo</strong></th><th><strong>Fecha de hallazgo</strong></th><th><strong>Hallazgo</strong></th></tr>'''
            for line in data.line_ids:
                nc_name = line.nc_id.name if line.nc_id else ''
                line_date = line.datetime.strftime('%d/%m/%Y') if line.datetime else ''
                data_tmp += line_row.format(line.name, nc_name, line_date, line.found)
        data_tmp = data_tmp + "</table></div>"
        return data_tmp

    resource = fields.Html(
        string='Manejo de los recursos',
    )
    resource_description = fields.Text(
        string='Interpretación',
    )

    risk = fields.Html(
        string='Riesgos y oportunidades',
        readonly=True,
        store=True,
    )
    risk_description = fields.Text(
        string='Interpretación',
    )

    def generate_risk(self):
        if self.is_last:
            matrix_1 = self.env['matrix.matrix'].search(
                [('date_validate', '>=', self.date_ini), ('date_validate', '<=', self.date_fin), ('state', '=', 'validate_ok'), ('type', '=', 'risk')], order='date_validate asc', limit=1)
            matrix_2 = self.env['matrix.matrix'].search(
                [('date_validate', '>=', self.date_ini), ('date_validate', '<=', self.date_fin), ('state', '=', 'validate_ok'), ('type', '=', 'opportunity')], order='date_validate asc', limit=1)
            matrix_ids = matrix_1 + matrix_2
        else:
            matrix_ids = self.env['matrix.matrix'].search(
                [('date_validate', '>=', self.date_ini), ('date_validate', '<=', self.date_fin), ('state', '=', 'validate_ok')], order='date_validate desc',)
        data_tmp = ""
        for matrix in matrix_ids:
            data_tmp = data_tmp + "<div style='margin-bottom:20px;'><table class='table table-bordered'>"
            type = dict(matrix._fields['type'].selection).get(matrix.type)
            link = ("<a data-oe-id=%s data-oe-model='matrix.matrix' href=#id=%s&model=matrix.matrix>%s</a>") % (
                matrix.id, matrix.id, type+": "+matrix.name)
            data_tmp += ("<tr><td colspan='3'>%s</td><tr>") % (link)
            if matrix.line_ids:
                data_tmp += "<tr><th><strong>Probabilidad</strong></th><th><strong>Descripción</strong></th><th><strong>Valor</strong></th></tr>"
            for line in matrix.line_ids:
                name = line.name if line.name else ''
                description = line.description if line.description else ''
                ntr = str(line.ntr) if line.ntr else ''
                data_tmp += "<tr><td>"+name+"</td><td>"+description+"</td><td>"+ntr+"</td></tr>"
            data_tmp += "</table></div>"
            
        return data_tmp

    improve_action_ids = fields.Many2many('mgmtsystem.action', string='Acciones de mejora', relation='mgmt_review_improve_action_rel')
    improve_action = fields.Html(
        string='Acciones de mejora',
        readonly=True,
        store=True,
    )
    improve_action_des = fields.Text(
        string='Interpretación',
    )

    def generate_improve_action(self):
        actions = self.env['mgmtsystem.action'].search([('type_action_id', '=', 'Acción de mejora'), (
            'date_open', '>=', self.date_ini), ('date_open', '<=', self.date_fin)])
        ac_temp = ''
        ac_temp = ac_temp + \
            "<div style='margin-bottom:20px;'><table class='table table-bordered'><tr style='align=center'><th>Acción</th><th>Responsable</th><th>Descripción</th><th>Estado</th></tr>"
        for ac in self.improve_action_ids:
            state = dict(self._fields['state'].selection).get(self.state)
            link = ("<a data-oe-id=%s data-oe-model='mgmtsystem.action' href=#id=%s&model=mgmtsystem.action>%s</a>") % (
                ac.id, ac.id, ac.name)
            ac_temp += "<tr><td>" + link + "</td><td>" + ac.user_id.name + \
                "</td><td>" + ac.description + "</td><td>" + state + "</td></tr>"
        ac_temp += "</table></div>"
        return ac_temp

    indicator = fields.Html(
        string='Indicadores',
        readonly=True,
        store=True,
    )
    indicator_description = fields.Text(
        string='Interpretación',
    )

    def generate_indicator(self):
        indicators = self.env['mgmtsystem.indicator'].search(
            [('start_date', '>=', self.date_ini), ('start_date', '<=', self.date_fin)])
        ac_temp = ''
        ac_temp = ac_temp + \
            "<table class='table table-bordered'><tr style='align=center'><th>Nombre</th><th>Objetivo</th><th>Frecuencia de medición</th></tr>"
        for ac in indicators:
            link = ("<a data-oe-id=%s data-oe-model='mgmtsystem.indicator' href=#id=%s&model=mgmtsystem.indicator>%s</a>") % (
                ac.id, ac.id, ac.name)
            m = ac.history_ids[len(ac.history_ids) -
                               1] if ac.history_ids else False
            meditions = ''
            # if m:
            #     meditions = "<div style='margin-bottom:20px;'><table class='table table-bordered'><th>Fecha</th><th>Valor esperado</th><th>Valor obtenido</th><th>Diferencia</th>"
            #     diff = str(m.expected_result - m.real_result)
            #     date = m.date.strftime('%d/%m/%Y') if m.date else ''
            #     meditions += "<tr><td>" + date + "</td><td>" + str(m.expected_result) + \
            #         "</td><td>" + str(m.real_result) + \
            #         "</td><td>" + str(diff) + "</td></tr>"
            #     meditions += "</table>"
            ac_temp += ("<tr><td>%s</td><td>%s</td><td>%s</td></tr>") % (
                link, ac.target_id.name, ac.measurement_frequency.name)
        ac_temp += "</table></div>"
        return ac_temp

    def update_data(self):
        if not self.date_ini and not self.date_fin and not self.is_last:
            return
        # ACTUALIZAR DATOS
        self.foda = self.generate_foda()
        self.target = self.generate_target()
        self.nonconformity_action = self.generate_nonconformity_action()
        self.audit = self.generate_audit()
        self.risk = self.generate_risk()
        self.suppliers_info = self.generate_suppliers()
        self.improve_action = self.generate_improve_action()
        self.process = self.generate_process()
        self.indicator = self.generate_indicator()
