# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockInspectionItem(models.Model):
    _name = 'stock.inspection.item'
    _description = 'Criterio de inspección'

    name = fields.Char(string='Nombre')
    inspection_id = fields.Many2one('stock.inspection', string='Inspección')


class StockInspection(models.Model):
    _name = 'stock.inspection'
    _inherit = 'mgmtsystem.validation.mail'
    _description = 'Inspección de compras'

    # inspection_date = fields.Date(string='Fecha de evaluación')

    name = fields.Char(string='Nombre')
    item_ids = fields.One2many(
        'stock.inspection.item', 'inspection_id', string='Criterios')


class PickingInspectionItem(models.Model):
    _name = 'stock.picking.inspection.item'
    _description = 'Criterio de inspección de compra'

    name = fields.Char(string='Nombre')

    yes = fields.Boolean(string='Sí')
    no = fields.Boolean(string='No')
    no_apply = fields.Boolean(string='No aplica')
    inspection_picking_id = fields.Many2one(
        'stock.picking.inspection', string='Recepción')

    @api.onchange('yes')
    def _onchange_yes(self):
        if self.yes:
            self.no = False
            self.no_apply = False

    @api.onchange('no')
    def _onchange_no(self):
        if self.no:
            self.yes = False
            self.no_apply = False

    @api.onchange('no_apply')
    def _onchange_no_apply(self):
        if self.no_apply:
            self.yes = False
            self.no = False


class PickingInspection(models.Model):
    _name = 'stock.picking.inspection'
    _description = 'Inspección de compras'
    _rec_name = 'inspection_id'

    inspection_id = fields.Many2one('stock.inspection', string='Inspección', domain="[('state','=','validate_ok')]")
    inspection_date = fields.Datetime(string='Fecha y hora de evaluación')
    employee_id = fields.Many2one('hr.employee', string='Evaluador')
    observations = fields.Text(string='Observaciones')
    item_ids = fields.One2many('stock.picking.inspection.item', 'inspection_picking_id', string='Criterios')
    
    picking_id = fields.Many2one('stock.picking', string='Recepción')

    @api.onchange('inspection_id')
    def _onchange_inspection_id(self):
        for each in self:
            item_ids = []
            if each.inspection_id:
                names = [x.name for x in each.inspection_id.item_ids]
                for name in names:
                    item_id = self.env['stock.picking.inspection.item'].create({
                        'name': name,
                        'inspection_picking_id': each.id,
                    })
                    item_ids.append(item_id.id)
            each.item_ids = [(6, 0, tuple(item_ids))]
            

    def print_evaluation(self):
        return self.env.ref('stock_inspection.action_report_stock_picking_inspection').report_action(self.id)


class Picking(models.Model):
    """ Hereda del modelo stock.picking
    """
    _inherit = 'stock.picking'

    inspection_ids = fields.One2many(
        'stock.picking.inspection', 'picking_id', string='Evaluaciones')

    # inspection_count = fields.Integer(
    #     string=u'Fichas',
    #     compute='_compute_inspection_count',
    #     store=False,
    # )

    inspection_count = fields.Boolean(string='A')

    return_date = fields.Date(string='Fecha de devolución al cliente')

    # def _compute_inspection_count(self):
    #     for record in self:
    #         data = record.env['stock_inspection.stock_inspection'].search([('stock_picking_id', '=', record.id)])
    #         count = len(data)
    #         record['inspection_count'] = count


class stock_inspectionLine(models.Model):
    """ Mostrará los criterios
    """
    _name = 'stock_inspection.stock_inspection.line'
    _description = 'Linea de inspección de compras'

    # name = fields.Char(string=u'Nombre', required=True)

    complete_name = fields.Text(
        string=u'Criterio de inspección', required=True)

    criterio = fields.Many2one(
        string=u'Calificación', comodel_name='stock_inspection.stock_inspection', ondelete='cascade')

    qualification = fields.Selection(
        string=u'Criterio',
        required=True,
        selection=[('SI', 'Si'), ('NO', 'No'), ('na', 'N/A')],
        default='na'
    )


class criterio(models.Model):
    """ Guardará los criterios, depende de cada empresa crear sus criterios
    """
    _name = 'stock_inspection.criterio'
    _description = "Criterio de compra"

    # name = fields.Char(string=u'Nombre', required=True)

    complete_name = fields.Text(string=u'Descripción', required=True)


class stockInspection(models.Model):
    """ Modelo de ficha para compras
    """
    _name = 'stock_inspection.stock_inspection'
    _description = "Stock inspection"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    # def _order_compra(self):
    #     # purchase order
    #     po = self.env['stock.picking'].browse(self._context.get("active_id"))
    #     # Funcion que obtenga el valor de stock.picking -> inspection_count
    #     inspec_count = po.inspection_count + 1
    #     # print ("INSPECT COUNT ", inspec_count)
    #     secuence = ""
    #     if (inspec_count):
    #         secuence = '000' + str(inspec_count)
    #     elif(inspec_count > 9 and inspec_count < 100):
    #         secuence = '00'+str(inspec_count)
    #     res = po.name+'/'+secuence if po.name and secuence else ''
    #     return res

    def _partner_compra(self):
        po = self.env['stock.picking'].browse(self._context.get("active_id"))
        return po.partner_id

    def _default_stock_picking(self):
        sp = self.env['stock.picking'].browse(self._context.get('active_id'))
        return sp

    def _facture_purchase(self):
        po = self.env['stock.picking'].browse(self._context.get("active_id"))

        fact = self.env['account.invoice'].search([('origin', '=', po.origin)])
        # print ("FACTURAS ????", fact)

        return po.origin
        # return fact

    stock_picking_id = fields.Many2one(
        string=u'ID stock', comodel_name='stock.picking', required=True, default=_default_stock_picking)

    # codigo
    name = fields.Char(string=u'Código',
                       help="Fichas relacionadas a la orden de compra")

    # fecha
    date_inspection = fields.Datetime(
        string=u'Fecha de revisión', default=fields.Datetime.now, required=True)

    # id el proveedor
    # proveedor_id = fields.Many2one(string=u'Proveedor', comodel_name='res.partner')     # el proveedor
    proveedor_ids = fields.Many2one(string=u'Proveedor', comodel_name='res.partner',
                                    default=_partner_compra, required=True)     # el proveedor

    # user id
    user_ids = fields.Many2one(
        string=u'Responsable', comodel_name='res.users', required=True)

    # factura id
    purchase_order_id = fields.Char(
        string=u'Orden de pedido', comodel_name='stop.picking', default=_facture_purchase, required=True)

    # Una nota para la inspeccion
    note = fields.Text(string=u'NOTA')

    # Muestra todos los criterios creados
    # TODO: En la interfaz no permite añadir un criterio desde la ficha !
    criterio_ids = fields.One2many(string=u'Criterios', comodel_name='stock_inspection.stock_inspection.line', inverse_name='criterio',
                                   default=lambda self: self._default_criterio_line_ids()
                                   )

    state = fields.Selection(
        string=u'Estado',
        selection=[('draft', 'Previo'), ('validate', 'Culminado')],
        default='draft',
    )
    # name_secuence = self.name + '0x'

    def _default_criterio_line_ids(self):
        """ Devuelve todos los criterios..
        """

        crit = self.env['stock_inspection.criterio'].search([])

        lines = [(5, 0, 0)]
        # print ("AQUI DATOSSSSSSSSSSSSS")
        for ct in crit:
            # print("criterios ", ct.complete_name)
            data = {
                # 'name': ct.name,
                'complete_name': ct.complete_name,
                'qualification': 'na',
            }
            lines.append((0, 0, data))
        return lines

    def change_state_validate(self):
        """ Cambia el estado de evaluate a validate.
        Esto culmina todo el proceso
        """
        self.state = 'validate'
