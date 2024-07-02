from odoo import models, fields, api


class ExternalIssueCreate(models.TransientModel):
    _name = 'mgmtsystem.context.external_issue.create_wizard'

    f1_name = fields.Char(string='Nombre')
    f1_desc = fields.Text(string='Descripción')
    f1_rel = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string='Puntuación', index=True)

    f2_name = fields.Char(string='Nombre')
    f2_desc = fields.Text(string='Descripción')
    f2_rel = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string='Puntuación', index=True)

    f3_name = fields.Char(string='Nombre')
    f3_desc = fields.Text(string='Descripción')
    f3_rel = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string='Puntuación', index=True)

    f4_name = fields.Char(string='Nombre')
    f4_desc = fields.Text(string='Descripción')
    f4_rel = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string='Puntuación', index=True)

    f5_name = fields.Char(string='Nombre')
    f5_desc = fields.Text(string='Descripción')
    f5_rel = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string='Puntuación', index=True)

    state = fields.Selection(
        selection=[
            ('step1', 'Step 1'),
            ('step2', 'Step 2'),
            ('step3', 'Step 3'),
            ('step4', 'Step 4'),
            ('step5', 'Step 5'),
        ],
        string="Fuerza",
        default="step1",
        readonly=True
    )

    def action_step1(self):
        self.state = 'step1'
        return {"type": "set_scrollTop"}

    def action_step2(self):
        self.state = 'step2'
        return {"type": "set_scrollTop"}

    def action_step3(self):
        self.state = 'step3'
        return {"type": "set_scrollTop"}

    def action_step4(self):
        self.state = 'step4'
        return {"type": "set_scrollTop"}

    def action_step5(self):
        self.state = 'step5'
        return {"type": "set_scrollTop"}

    def action_finish(self):
        external_issue = self.env['mgmtsystem.context.external_issue']
        f1, = self.env["mgmtsystem.context.force"].search(
            [('code', '=', 'F1')])
        external_issue.create({
            'name': self.f1_name,
            'description': self.f1_desc,
            'relevance': self.f1_rel,
            'force': f1.id
        })
        f2, = self.env["mgmtsystem.context.force"].search(
            [('code', '=', 'F2')])
        external_issue.create({
            'name': self.f2_name,
            'description': self.f2_desc,
            'relevance': self.f2_rel,
            'force': f2.id
        })
        f3, = self.env["mgmtsystem.context.force"].search(
            [('code', '=', 'F3')])
        external_issue.create({
            'name': self.f3_name,
            'description': self.f3_desc,
            'relevance': self.f3_rel,
            'force': f3.id
        })
        f4, = self.env["mgmtsystem.context.force"].search(
            [('code', '=', 'F4')])
        external_issue.create({
            'name': self.f4_name,
            'description': self.f4_desc,
            'relevance': self.f4_rel,
            'force': f4.id
        })
        f5, = self.env["mgmtsystem.context.force"].search(
            [('code', '=', 'F5')])
        external_issue.create({
            'name': self.f5_name,
            'description': self.f5_desc,
            'relevance': self.f5_rel,
            'force': f5.id
        })

        tree_view_id = self.env.ref('mgmtsystem_context.context_external_issue_view_tree').ids
        form_view_id = self.env.ref('mgmtsystem_context.context_external_issue_view_form').ids

        return {
            'name': 'Abrir',
            'view_mode': 'tree',
            'views': [[tree_view_id, 'tree'], [form_view_id, 'form']],
            'res_model': 'mgmtsystem.context.external_issue',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
