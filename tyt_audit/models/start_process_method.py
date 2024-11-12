# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

from datetime import tzinfo, date, datetime, timedelta
import pandas as pd
import logging
_logger = logging.getLogger(__name__)

class Plan(models.Model):
    _inherit = "audit.plan"

    # Campo para evitar duplicados
    is_process_started = fields.Boolean(
        string='Proceso Iniciado',
        default=False,
        readonly=True
    )

    def start_process(self):
        for plan in self:
            _logger.info(f"Iniciando el proceso para el plan: {plan.name} (ID: {plan.id})")
            print(f"Iniciando el proceso para el plan: {plan.name} (ID: {plan.id})")

            #if plan.is_process_started:
                #raise UserError(_("El proceso ya ha sido iniciado para este registro."))

            if not plan.audit_plan_tyt_auditor_id:
                raise UserError(_("Debe asignar un 'Cronograma - Auditores' antes de iniciar el proceso."))

            _logger.info(f"Auditor asociado: {plan.audit_plan_tyt_auditor_id.name} (ID: {plan.audit_plan_tyt_auditor_id.id})")
            print(f"Auditor asociado: {plan.audit_plan_tyt_auditor_id.name} (ID: {plan.audit_plan_tyt_auditor_id.id})")

            # IDs de los sitios
            SITE_GUADALAJARA_ID = 1
            SITE_HERMOSILLO_ID = 2
            SITE_PUEBLA_CAT_ID = 10
            SITE_PUEBLA_ID = 9
            SITE_QUERETARO_ID = 8
            SITE_M_TAPIA_ID = 7
            SITE_M_ARTEAGA_ID = 5
            SITE_MERIDA_ID = 3



            # Definir los datos de los registros a crear basados en nombres únicos de sitios
            schedule_data = [
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_101').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_102').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_103').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_104').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },


                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_201').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_202').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_203').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_204').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_301').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_302').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_303').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_304').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_401').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_402').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_403').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_404').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_405').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_406').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },                
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_501').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_502').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_503').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_504').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_505').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_506').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_507').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_508').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_509').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_601').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_602').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_603').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_604').id,
                    'sites_id': SITE_GUADALAJARA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_101').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_102').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_103').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_104').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },


                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_201').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_202').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_203').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_204').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_301').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_302').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_303').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_304').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_401').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_402').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_403').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_404').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_405').id,
                    'sites_id': SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_406').id,
                    'sites_id': SITE_HERMOSILLO_ID,
                },                 
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_501').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_502').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_503').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_504').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_505').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_506').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_507').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_508').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_509').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_601').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_602').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_603').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_604').id,
                    'sites_id':SITE_HERMOSILLO_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_101').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_102').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_103').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_104').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },


                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_201').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_202').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_203').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_204').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_301').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_302').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_303').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_304').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_401').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_402').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_403').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_404').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_405').id,
                    'sites_id': SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_406').id,
                    'sites_id': SITE_PUEBLA_CAT_ID,
                }, 
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_501').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_502').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_503').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_504').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_505').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_506').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_507').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_508').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_509').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_601').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_602').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_603').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_604').id,
                    'sites_id':SITE_PUEBLA_CAT_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_101').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_102').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_103').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_104').id,
                    'sites_id':SITE_PUEBLA_ID,
                },


                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_201').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_202').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_203').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_204').id,
                    'sites_id':SITE_PUEBLA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_301').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_302').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_303').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_304').id,
                    'sites_id':SITE_PUEBLA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_401').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_402').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_403').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_404').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_405').id,
                    'sites_id': SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_406').id,
                    'sites_id': SITE_PUEBLA_ID,
                }, 
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_501').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_502').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_503').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_504').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_505').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_506').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_507').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_508').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_509').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_601').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_602').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_603').id,
                    'sites_id':SITE_PUEBLA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_604').id,
                    'sites_id':SITE_PUEBLA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_101').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_102').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_103').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_104').id,
                    'sites_id':SITE_QUERETARO_ID,
                },


                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_201').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_202').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_203').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_204').id,
                    'sites_id':SITE_QUERETARO_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_301').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_302').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_303').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_304').id,
                    'sites_id':SITE_QUERETARO_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_401').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_402').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_403').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_404').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_405').id,
                    'sites_id': SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_406').id,
                    'sites_id': SITE_QUERETARO_ID,
                }, 
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_501').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_502').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_503').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_504').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_505').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_506').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_507').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_508').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_509').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_601').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_602').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_603').id,
                    'sites_id':SITE_QUERETARO_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_604').id,
                    'sites_id':SITE_QUERETARO_ID,
                },                
            
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_101').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_102').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_103').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_104').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },


                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_201').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_202').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_203').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_204').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_301').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_302').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_303').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_304').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_401').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_402').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_403').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_404').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_405').id,
                    'sites_id': SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_406').id,
                    'sites_id': SITE_M_TAPIA_ID,
                }, 
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_501').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_502').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_503').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_504').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_505').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_506').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_507').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_508').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_509').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_601').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_602').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_603').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_604').id,
                    'sites_id':SITE_M_TAPIA_ID,
                },          


                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_101').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_102').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_103').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_104').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },


                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_201').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_202').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_203').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_204').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_301').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_302').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_303').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_304').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_401').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_402').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_403').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_404').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_405').id,
                    'sites_id': SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_406').id,
                    'sites_id': SITE_M_ARTEAGA_ID,
                }, 
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_501').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_502').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_503').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_504').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_505').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_506').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_507').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_508').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_509').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_601').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_602').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_603').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_604').id,
                    'sites_id':SITE_M_ARTEAGA_ID,
                },


                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_101').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_102').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_103').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_1').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_104').id,
                    'sites_id':SITE_MERIDA_ID,
                },


                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_201').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_202').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_203').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_2').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_204').id,
                    'sites_id':SITE_MERIDA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_301').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_302').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_303').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_3').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_304').id,
                    'sites_id':SITE_MERIDA_ID,
                },

                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_401').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_402').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_403').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_404').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_405').id,
                    'sites_id': SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_4').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_406').id,
                    'sites_id': SITE_MERIDA_ID,
                }, 
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_501').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_502').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_503').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_504').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_505').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_506').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_507').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_508').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_5').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_509').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_601').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_602').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_603').id,
                    'sites_id':SITE_MERIDA_ID,
                },
                {
                    'description_id': self.env.ref('tyt_audit.schedule_plan_description_6').id,
                    'activity_id': self.env.ref('tyt_audit.schedule_plan_activity_604').id,
                    'sites_id':SITE_MERIDA_ID,
                },
            ]
            #####
            # Modificación OPCIONAL
            #####
            # Antes de iniciar la iteración en "schedule_data" vamos a borrar todos los registros de "audit.plan.schedule"(self.schedule_ids) de este registro de audit.plan 
            # Borrar todos los cronogramas generados nos permitirá sobrescribir los datos generados por el metodo, en caso realicemos modificaciones en "Cronograma de auditoría - Auditores"
            
            for data in schedule_data:
                site = self.env['x_sitios'].browse(data['sites_id'])
                _logger.info(f"Procesando sitio: {site.x_name} (ID: {site.id})")
                print(f"Procesando sitio: {site.x_name} (ID: {site.id})")

                existing_schedule = self.env['audit.plan.schedule'].search([
                    ('audit_plan_id', '=', plan.id),
                    ('description_id', '=', data['description_id']),
                    ('activity_id', '=', data['activity_id']),
                    ('sites_id', '=', data['sites_id']),
                ], limit=1)

                if existing_schedule:
                    _logger.info(f"Ya existe un schedule para sitio '{site.x_name}' con ID {existing_schedule.id}.")
                    print(f"Ya existe un schedule para sitio '{site.x_name}' con ID {existing_schedule.id}.")
                    continue  # Omitir la creación si ya existe

                # Obtener los datos de audit.plan.tyt.auditor.schedule según sites_id
                auditor_schedules = plan.audit_plan_tyt_auditor_id.schedule_ids.filtered(
                    lambda s: s.tyt_sites_id.id == data['sites_id']
                )

                # Depuración
                _logger.info(f"Auditor Schedules para sitio ID {data['sites_id']}: {auditor_schedules.ids}")
                print(f"Auditor Schedules para sitio ID {data['sites_id']}: {auditor_schedules.ids}")

                if not auditor_schedules:
                    _logger.warning(f"No hay schedules configurados para el sitio ID {data['sites_id']}.")
                    raise UserError(_("No hay datos de auditoría configurados para el sitio seleccionado."))

                # Calcular total_weeks sumando 'total_sum' de todos los schedules relacionados
                total_weeks = sum(aud.total_sum for aud in auditor_schedules)
                _logger.info(f"Total semanas para sitio ID {data['sites_id']}: {total_weeks}")
                print(f"Total semanas para sitio ID {data['sites_id']}: {total_weeks}")

                # Obtener todos los auditores responsables
                auditors = self.env['res.partner'].browse()
                for aud_schedule in auditor_schedules:
                    auditors |= aud_schedule.responsible_auditors_id

                _logger.info(f"Auditores responsables: {auditors.mapped('name')}")
                print(f"Auditores responsables: {auditors.mapped('name')}")

                # Crear el registro en audit.plan.schedule
                new_schedule = self.env['audit.plan.schedule'].create({
                    'audit_plan_id': plan.id,
                    'description_id': data['description_id'],
                    'activity_id': data['activity_id'],
                    'sites_id': data['sites_id'],
                    'responsible_auditors_id': [(6, 0, auditors.ids)],
                    'total_weeks': total_weeks,
                    'name': f"{plan.name} - Sitio: {site.x_name}",
                })

                _logger.info(f"Nuevo schedule creado: ID {new_schedule.id} para el sitio {site.x_name}")
                print(f"Nuevo schedule creado: ID {new_schedule.id} para el sitio {site.x_name}")

            # Marcar el proceso como iniciado
            plan.is_process_started = True

            # Mensaje de confirmación
            plan.message_post(body=_("El proceso ha sido iniciado y los registros de cronograma han sido creados."))

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }