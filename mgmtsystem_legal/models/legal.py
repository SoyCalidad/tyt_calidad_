# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class res_partner(models.Model):
    _inherit = 'res.partner'

    purchase_warn = fields.Selection(
        WARNING_MESSAGE, 'Purchase Order', help=WARNING_HELP, required=False, default="no-message")


class LegalType(models.Model):
    _name = "legal.type"
    _description = "Tipo de requisitos legales"

    name = fields.Char(
        string=u'Nombre',
        required=True,
    )
    description = fields.Text(
        string=u'Descripción',
    )
    legal_ids = fields.One2many(
        string=u'Requisitos',
        comodel_name='legal.legal',
        inverse_name='type_id',
    )
    legals_count = fields.Integer(
        string=u'# de requisitos',
        compute='_compute_legals_count',
        store=False,
    )

    @api.depends('legal_ids')
    def _compute_legals_count(self):
        for record in self:
            record.legals_count = len(record.legal_ids) or 0


class Legal(models.Model):
    _name = "legal.legal"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'mgmtsystem.version']
    _description = "Requisitos legales"

    user_id = fields.Many2one(
        comodel_name='res.users',
        string=u'Responsable',
        default=lambda self: self.env.user)
    name = fields.Char(
        string=u'Titulo',
        required=True,
    )
    type_id = fields.Many2one(
        string=u'Tipo',
        comodel_name='legal.type',
        ondelete='cascade',
    )
    entity_id = fields.Many2one(
        string=u'Entidad',
        comodel_name='res.partner',
        ondelete='restrict',
    )
    reference = fields.Char(
        string=u'Referencia',
    )
    date_release = fields.Date(
        string=u'Fecha de publicación',
    )
    is_outsourcing = fields.Boolean(
        string=u'¿Tercerización?',
    )
    partner_id = fields.Many2one(
        string=u'Responsable',
        comodel_name='res.partner',
        ondelete='restrict',
    )
    resume = fields.Text(
        string=u'Resumen',
    )
    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('validate', 'Validado'),
            ('caducated', 'Caducado'),
            ('cancel', 'Obsoleto'),
        ],
        default='elaborate',
        copy=False,
    )

    article_ids = fields.One2many(
        string=u'Articulos',
        comodel_name='legal.article',
        inverse_name='legal_id',
        copy=True,
    )
    articles_count = fields.Integer(
        string=u'# de articulos',
        compute='_compute_articles_count',
        store=False,
    )
    action_id = fields.Many2one(
        'mgmtsystem.action',
        string='Cómo se cumplirá')

    @api.depends('article_ids')
    def _compute_articles_count(self):
        for record in self:
            record.articles_count = len(record.article_ids) or 0

    def send_validate(self):
        for article in self.article_ids:
            article.send_validate()
        self.state = 'validate'

    def send_caducated(self):
        for article in self.article_ids:
            article.send_caducated()
        self.state = 'caducated'

    parent_edition = fields.Many2one(
        comodel_name='legal.legal', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='legal.legal', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def button_new_version(self):
        self.ensure_one()
        self._copy_edition()
        revno = self.version
        self.write({
            'version': revno + 1,
            'state': 'elaborate',
            'name': self.name
        })
    
    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_legal.legal_legal_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class Article(models.Model):
    _name = "legal.article"

    legal_id = fields.Many2one(
        string=u'Requisito legal',
        comodel_name='legal.legal',
        ondelete='restrict',
        required=True,
    )

    name = fields.Char(
        string=u'Nombre',
        required=True,
    )
    resume = fields.Text(
        string=u'Resumen',
    )
    stakeholders = fields.Char(
        string=u'Stakeholders',
    )
    partner_id = fields.Many2one(
        string=u'Responsable',
        comodel_name='res.partner',
        ondelete='restrict',
    )
    type_id = fields.Many2one(
        string=u'Tipo',
        related='legal_id.type_id',
        readonly=True,
        store=False
    )
    entity_id = fields.Many2one(
        string=u'Entidad',
        related='legal_id.entity_id',
        readonly=True,
        store=False
    )
    date_release = fields.Date(
        string=u'Fecha de publicación',
        related='legal_id.date_release',
        readonly=True,
        store=False
    )
    state = fields.Selection(
        related='legal_id.state',
        readonly=True,
        store=False
    )

    def send_validate(self):
        self.state = 'validate'

    def send_caducated(self):
        self.state = 'caducated'

    attachs_count = fields.Integer(
        string=u'# de adjuntos',
        compute='_compute_has_attachments',
        store=False,
    )

    @api.depends('legal_id')
    def _compute_has_attachments(self):
        for each in self:
            nbr_attach = self.env['legal.article.document'].search_count([
                '&', ('res_model', '=', 'legal.article'), ('res_id', '=', each.id)])
            each.attachs_count = nbr_attach or 0
            each.has_attachments = bool(nbr_attach)

    has_attachments = fields.Boolean(
        'Tiene documentos', compute='_compute_has_attachments', store=False)

    def action_see_attachments(self):
        domain = [
            '&', ('res_model', '=', 'legal.article'), ('res_id', '=', self.id), ]
        attachment_view = self.env.ref(
            'mgmtsystem_legal.view_document_file_kanban_article_document')
        return {
            'name': _('Adjuntos'),
            'domain': domain,
            'res_model': 'legal.article.document',
            'type': 'ir.actions.act_window',
            'view_id': attachment_view.id,
            'views': [(attachment_view.id, 'kanban'), (False, 'form')],
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Haga clic para cargar archivos de evidencia
                    </p><p>
                        Utilice esta función para almacenar cualquier archivo.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % ('legal.article', self.id)
        }


class ArticleDocument(models.Model):
    _name = 'legal.article.document'
    _description = "Documento de articulo"
    _inherits = {
        'ir.attachment': 'ir_attachment_id',
    }
    _order = "priority desc, id desc"

    ir_attachment_id = fields.Many2one(
        'ir.attachment', string='Documentos adjuntos', required=True, ondelete='cascade')
    active = fields.Boolean('Activo', default=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Bajo'),
        ('2', 'Alto'),
        ('3', 'Muy alto')], string="Prioridad", help='Da la secuencia')
