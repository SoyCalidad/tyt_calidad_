from odoo import api, fields, models

class ProcessUTils(models.TransientModel):
    _name = 'mgmt.process.utils'
    _description = 'ProcessUTils'

    def update_categ(self):
        # self.env['mgmt.categ'].search([], order='create_date desc')

        process_ids = self.env['mgmt.process'].search([('active', '=', True)])

        for process in process_ids:
            if process.categ_id:
                categ_id = self.env['mgmt.categ'].search([('name','=',process.categ_id.name)], order='create_date desc', limit=1)
                process.categ_id = categ_id



    