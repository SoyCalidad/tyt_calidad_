from odoo import api, fields, models


class ProcessCategExport(models.Model):
    _inherit = 'mgmt.categ'

    # @api.model
    # def create(self, values):
    #     res = super(ProcessCategExport, self).create(values)
    #     self.env['mgmt.categ.dummy'].create({
    #         'categ': res.id,
    #     })
    #     return res
    
    @api.model_create_multi
    def create(self, vals_list):
        # Crear todos los registros de mgmt.categ utilizando el método super
        categ_records = super(ProcessCategExport, self).create(vals_list)

        # Preparar los valores para los registros de mgmt.categ.dummy
        dummy_vals = []
        for categ in categ_records:
            dummy_vals.append({
                'categ': categ.id,
            })

        # Crear todos los registros de mgmt.categ.dummy de una sola vez
        self.env['mgmt.categ.dummy'].create(dummy_vals)
        return categ_records

    
    def export_process(self):
        process = self.env['mgmt.categ'].search([])
        dummy = self.env['mgmt.categ.dummy'].search([])
        dummy_ids = [x.id for x in dummy]
        for p in process:
            if p.id not in dummy_ids:
                self.env['mgmt.categ.dummy'].create({
                    'categ': p.id,
                })


class ProcessCategDummy(models.Model):
    _name = 'mgmt.categ.dummy'
    _description = 'Categoría de procesos'

    name = fields.Char(string='Nombre', related='categ.name')
    categ = fields.Many2one('mgmt.categ', string='Categorías')


class ProcessReportWizard(models.TransientModel):
    _name = 'mgmt.process.report.wizard'

    categ = fields.Many2many('mgmt.categ.dummy', string='Categorías')

    def action_print(self):
        ids_ = [x.categ.id for x in self.categ]
        datas = {
            'ids_': ids_,
            'is_wizard': True,
        }
        return self.env.ref('mgmtsystem_process.reporte_process').report_action(self, data=datas)
