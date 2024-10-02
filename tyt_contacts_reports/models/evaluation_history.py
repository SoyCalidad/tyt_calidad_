from odoo import api, models, fields


class Evaluation(models.Model):
    _inherit = 'res.partner.evaluation'

    is_tyt_evaluation = fields.Boolean(string='Is TYT Evaluation')


class History(models.Model):
    _inherit = 'res.partner.evaluation.history'

    is_tyt_evaluation = fields.Boolean(string='Is TYT Evaluation', related='evaluation_id.is_tyt_evaluation', store=True)
    evaluation_qualification = fields.Selection([
        ('a', 'A - Excepcional'),
        ('b', 'B - Aceptable'),
        ('c', 'C - Aceptable con prueba adicional'),
        ('d', 'D - Inaceptable'),
    ], string='Evaluation Qualification')

    def print_evaluation(self):
        if self.is_tyt_evaluation:
            return self.env.ref('tyt_contacts_reports.supplier_evaluation_verification_xlsx_report_action').report_action(self.id)
        return self.env.ref('mgmtsystem_partner_qualification.action_report_res_partner_evaluation').report_action(self.id)


class HistoryItem(models.Model):
    _inherit = 'res.partner.evaluation.history.item'

    is_tyt_evaluation = fields.Boolean(string='Is TYT Evaluation', related='history_id.is_tyt_evaluation', store=True)

    @api.depends('history_line_ids.scala', 'history_line_ids.evaluation_item_line_value')
    def _compute_qualification_item(self):
        for record in self:
            if not record.history_line_ids:
                record.qualification_item = 0
                record.weight_total = 0
            qua = qua_max = 0.0

            if record.is_tyt_evaluation:
                for line in record.history_line_ids:
                    record.qualification_item = record.qualification_item + line.evaluation_item_line_value
            else:
                for line in record.history_line_ids:
                    line._onchange_scala()
                    qua = qua + line.qualification_line
                    qua_max = qua_max + line.line_id.weight*5
                record.weight_total = int(record.item_id.weight_total)
                record.qualification_item = (
                    qua*record.item_id.weight_total)/qua_max if qua_max > 0 else 0


class HistoryItemLine(models.Model):
    _inherit = 'res.partner.evaluation.history.item.line'

    evaluation_item_line_weight = fields.Float(string='Puntuación máxima', related='line_id.weight', store=True)
    evaluation_item_line_value = fields.Integer(string='Valor', required=True)

    @api.onchange('evaluation_item_line_value')
    def _onchange_evaluation_item_line_value(self):
        for record in self:
            if not (0 <= record.evaluation_item_line_value <= record.evaluation_item_line_weight):
                record.evaluation_item_line_value = 0
                return {
                    'warning': {
                        'title': "Valor fuera del rango",
                        'message': "El valor debe estar entre 0 y la puntuación máxima {}.".format(record.evaluation_item_line_weight),
                    }
                }
