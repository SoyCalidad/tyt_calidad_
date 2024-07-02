from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PartnerQualificationWizard(models.Model):
    _name = 'partner.qualification.wizard'

    filter_by = fields.Selection([
        ('date', 'Fecha'),
        ('supplier', 'Proveedor'),
    ], string='Filtrar por', default='date')

    start_date = fields.Date(string='Desde')
    end_date = fields.Date(string='Hasta')

    supplier_ids = fields.Many2many(
        'res.partner', string='Proveedores', domain="[('supplier', '=', True)]")

    def action_print(self):
        if self.filter_by == 'date':
            evaluation_ids = self.env['res.partner.evaluation.history'].search(
                [('date_history', '>=', self.start_date or '1000-01-01'), ('date_history', '<=', self.end_date or '9999-12-31')], order='partner_id asc')
        elif self.filter_by == 'supplier':
            evaluation = []
            for supplier in self.supplier_ids:
                evaluation.extend(supplier.history_ids.ids)
            evaluation_ids = self.env['res.partner.evaluation.history'].browse(
                evaluation)
        else:
            raise ValidationError('Debe seleccionar un filtro')
        return self.env.ref('mgmtsystem_partner_qualification.action_report_res_partner_evaluation').report_action(evaluation_ids)
