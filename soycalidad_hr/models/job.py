import logging
from termios import OFDEL

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class HrJobMainSkill(models.Model):
    _name = 'hr.job.main_skill'
    _description = 'Competencias del puesto'

    name = fields.Char('Nombre', required=True)
    type = fields.Selection([
        ('generic', 'Genérica'),
        ('workteam', 'Trabajo en equipo'),
        ('personal', 'Personal'),
        ('strategic', 'Estratégica'),
    ], string='Tipo')


class Skill(models.Model):
    _inherit = 'hr.job.skill'

    def update_database_skills(self, names, type):
        # Creamos las competencias genéricas en la base de datos
        table = 'hr_job_{}_skill'.format(type)
        for name in names:
            self._cr.execute(
                """SELECT id FROM %s WHERE name = '%s'""" % (table, name))
            
            record = self._cr.fetchone()
            if record:
                record_id = record[0]
            if record:
                try:
                    self._cr.execute(
                        """INSERT INTO hr_job_main_skill (name, type) VALUES ('%s', '%s') RETURNING id""" % (name, type))
                    skill_id = self._cr.fetchone()[0]
                    self._cr.execute("""UPDATE %s SET main_skill_id = %s WHERE id = %s""" % (
                        table, skill_id, record_id))
                except Exception as e:
                    _logger.error(e)


class GenericSkill(models.Model):
    _inherit = 'hr.job.generic_skill'

    main_skill_id = fields.Many2one(
        'hr.job.main_skill', string='Competencia', domain='[("type", "=", "generic")]')

    def init(self):
        # Obtenemos las competencias genéricas
        generic_skills = self._cr.execute(
            """SELECT name FROM hr_job_generic_skill""")
        names = [t[0] for t in self.env.cr.fetchall()]
        # Creamos las competencias genéricas en la base de datos
        self.update_database_skills(names, 'generic')


class WorkteamSkill(models.Model):
    _inherit = 'hr.job.workteam_skill'

    main_skill_id = fields.Many2one(
        'hr.job.main_skill', string='Competencia', domain='[("type", "=", "teamwork")]')
    
    def init(self):
        # Obtenemos las competencias de trabajo en equipo
        generic_skills = self._cr.execute(
            """SELECT name FROM hr_job_generic_skill""")
        names = [t[0] for t in self.env.cr.fetchall()]
        # Creamos las competencias genéricas en la base de datos
        self.update_database_skills(names, 'workteam')


class PersonalSkill(models.Model):
    _inherit = 'hr.job.personal_skill'

    main_skill_id = fields.Many2one(
        'hr.job.main_skill', string='Competencia', domain='[("type", "=", "personal")]')
    
    def init(self):
        # Obtenemos las competencias personales
        generic_skills = self._cr.execute(
            """SELECT name FROM hr_job_personal_skill""")
        names = [t[0] for t in self.env.cr.fetchall()]
        # Creamos las competencias genéricas en la base de datos
        self.update_database_skills(names, 'personal')


class StrategicSkill(models.Model):
    _inherit = 'hr.job.strategic_skill'

    main_skill_id = fields.Many2one(
        'hr.job.main_skill', string='Competencia', domain='[("type", "=", "strategic")]')
    
    def init(self):
        # Obtenemos las competencias estratégicas
        generic_skills = self._cr.execute(
            """SELECT name FROM hr_job_strategic_skill""")
        names = [t[0] for t in self.env.cr.fetchall()]
        # Creamos las competencias genéricas en la base de datos
        self.update_database_skills(names, 'strategic')
