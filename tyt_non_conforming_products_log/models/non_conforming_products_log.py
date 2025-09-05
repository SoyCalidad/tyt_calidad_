from odoo import models, fields, api


class FrequencyOption(models.Model):
    _name = 'non.conforming.products.log.frequency'
    _description = 'Frequency Options'

    name = fields.Char(string="Frequency Option", required=True)
    
    
class NonConformingProductsLog(models.Model):
    _name = 'non.conforming.products.log'
    _description = 'Non-Conforming Products Log'
    
    site = fields.Many2one('tyt_studio.sites', string='Site', required=True)
    report_id = fields.Char(string='Report ID', required=True)
    campaign = fields.Many2one('marketing.campaign', string='Campaign', required=True)
    report_date = fields.Date(string='Report Date', required=True, default=fields.Date.today)
    line_number = fields.Char(string='Line Number', required=True)
    login = fields.Char(string='Login', required=True)
    complete_name = fields.Many2one('hr.employee', string='Complete Name', required=True)
    adjustment_cause = fields.Char(string='Adjustment Cause (PNC)', required=True)
    validation_date = fields.Date(string='Validation Date', required=True, default=fields.Date.today)
    
    proceed = fields.Boolean(string='Proceed', default=False)
    pnc_responsable = fields.Many2one('hr.employee', string='PNC Responsable', required=True)
    signed_adjustment = fields.Boolean(string='Signed Adjustment', default=False)
    general_amount = fields.Float(string='General Amount', required=True)
    weekly_amount = fields.Float(string='Weekly Amount', required=True)
    nominal_weeks = fields.Integer(string='Nominal Weeks (Discount)', required=True)
    frequency = fields.Many2one(
        'non.conforming.products.log.frequency',
        string="Frequency",
        help="Select or create a new frequency option"
    )
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date(string='End Date', required=True, default=fields.Date.today)
    
    coments = fields.Text(string='Coments')
    
    payments_ids = fields.One2many(
        'non.conforming.products.log.line', 'nonconformingproductslog_id', string='Payments',
        default=lambda self: [
            {'payment_number': 'Primer Pago'},
            {'payment_number': 'Segundo Pago'},
            {'payment_number': 'Tercer Pago'},
            {'payment_number': 'Cuarto Pago'}, 
            {'payment_number': 'Quinto Pago'},
        ]
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string="Status", default='draft')
    
    def action_confirm(self):
        self.ensure_one()
        self.write({'state': 'confirmed'})
        return True

    def action_cancel(self):
        self.ensure_one()
        self.write({'state': 'draft'})
        return {'type': 'ir.actions.act_window_close'}

    def action_draft(self):
        self.write({'state': 'draft'})
        
    @api.model
    def init(self):
        options = ['Daily', 'Weekly', 'Monthly']
        frequency_model = self.env['non.conforming.products.log.frequency']
        for option in options:
            if not frequency_model.search([('name', '=', option)]):
                frequency_model.create({'name': option})
                
class NonConformingProductsLogLine(models.Model):

    _name = 'non.conforming.products.log.line'
    _description = 'Log Line'
    
    nonconformingproductslog_id = fields.Many2one(
        'non.conforming.products.log', string='Remediation Log', required=True, ondelete='cascade'
    )
    
    payment_number = fields.Char(string='Payment Number', required=True)
    folio = fields.Char(string='Folio')
    date = fields.Date(string='Payment Date', default=fields.Date.today)
    amount = fields.Float(string='Amount')
    paymeny_status = fields.Selection([ ('pagado', 'Pagado'), ('no pagado', 'No Pagado')], string="Status", default='no pagado')
    responsable = fields.Many2one('hr.employee', string='Discount To')
    

    