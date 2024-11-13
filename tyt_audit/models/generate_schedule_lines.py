# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

from datetime import tzinfo, date, datetime, timedelta
import pandas as pd

class Plan(models.Model):
    _inherit = "audit.plan"

    def generate_schedule_lines(self):
        '''Use the pandas function date_range and generates
        maitenance_requests according frequency'''

        self.ensure_one() # Asegura que solo se está trabajando con un registro , ideal si el metodo se ejecuta desde una vista formulario y para un solo registro

        for schedule in self.schedule_ids:
            
            schedule.line_ids.unlink() # Elimina todas los registros fecha(audit.plan.schedule.line) asociados al registro "audit.plan.schedule" en "audit.plan" registro actual (self)

            #schedule.line_ids = [(5, 0, 0)] # elimina todos los registros existentes asociados al campo schedule_ids para el registro actual (self).
            
            start_date = self.start_date
            limit_date = self.limit_date
            freq = ''
            if self.new_frequency_id.years > 0:
                freq = pd.DateOffset(years=self.new_frequency_id.years)
            elif self.new_frequency_id.months > 0:
                freq = pd.DateOffset(months=self.new_frequency_id.months)
            elif self.new_frequency_id.weeks > 0:
                freq = pd.DateOffset(weeks=self.new_frequency_id.weeks)
            elif self.new_frequency_id.days > 0:
                freq = pd.DateOffset(days=self.new_frequency_id.days)
            dRan1 = pd.bdate_range(start=start_date, end=limit_date, freq=freq)
            new_lines = []
            for single_date in dRan1:
                # Crear un nuevo registro de line
                new_line = self.env['audit.plan.schedule.line'].create({
                    'schedule_id': schedule.id,  # Asignar al schedule actual
                    'name': f"{schedule.name} {single_date.strftime('%d/%m/%Y')}",
                    'scheduled_date': single_date.date(),
                })
                # Agregar el ID del nuevo line al listado
                new_lines.append(new_line.id)

            # Asignar todos los nuevos lines al schedule actual
            schedule.line_ids = [(6, 0, new_lines)]
                