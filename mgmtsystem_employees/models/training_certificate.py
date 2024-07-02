from odoo import api, fields, models
# from docx import Document
from pathlib import Path


class EmployeeCertificate(models.Model):
    _inherit = 'hr.employee'

    def get_certificate(self):
        pass

    def print_certficate(self):
        return self.env.ref('mgmtsystem_employees.action_report_training_certificate').report_action(self.id)


class TrainingCertificate(models.TransientModel):
    _name = 'mgmtsystem.plan.training.certificate.wizard'

    employee_ids = fields.Many2many('hr.employee', string='Empleados')

    def print_certficate(self):
        for each in self:
            ids = []
            for line in each.line_ids:
                if line.state_test == 'approved':
                    ids.append(line.id)
            if ids:
                return self.env.ref('mgmtsystem_employees.action_report_training_certificate').report_action(tuple(ids))



    def get_certificate(self):
        path = Path(__file__).absolute().parent.parent
        path1 = path / 'static' / 'docs' / 'OutputDoc.html'
        path2 = path / 'static' / 'docs' / 'new.pdf'

        pdfkit.from_file(str(path1), str(path2))

        # document = Document(path1)

        # paragraphs = []
        # for para in document.paragraphs:
        #     p = para.text
        #     paragraphs.append(p)

        # path2 = 'output.docx'
        # output = Document()
        # output.add_heading('A', 0)
        # for item in paragraphs:
        #     output.add_paragraph(item)
        # output.save(path2)
