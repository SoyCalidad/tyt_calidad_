# -*- coding: utf-8 -*-

from . import models

from .migrate_models import _migrate_models_with_sql
import logging 

_logger = logging.getLogger(__name__)


def _post_migrate_hook(env):
    
    # migrate models        
    _logger.info("Updating models------------")
    result_models = _migrate_models_with_sql(env) 
    
    if not result_models:
        _logger.warning("No se ejecutaron la migracion de los modelos")
        return
           
    users = env['res.users'].sudo().search([])
    update_user_len = 0
    for us in users:
        if hasattr(us, 'x_studio_empleado') and us.x_studio_empleado and not us.empleado:
            us.empleado = us.x_studio_empleado 
            update_user_len += 1
            
        if hasattr(us, 'x_studio_numero') and us.x_studio_numero and not us.numero:
            us.numero = us.x_studio_numero 
            update_user_len += 1

        if hasattr(us, 'x_studio_sitio') and us.x_studio_sitio and not us.sitio:
            sitio = env['tyt_studio.site'].browse(us.x_studio_sitio.id)
            if sitio:
                us.sitio = sitio
                update_user_len += 1
            else:
                _logger.warning(f"En el usuario {us} no se podido actualizar el campo sitio, ya no existe el x_studio_sitio_id {us.x_studio_sitio.id} en tyt_studio")
    _logger.info(f"Updated {update_user_len/3} users")

    departments = env['hr.department'].sudo().search([])
    update_department_len = 0
    for dep in departments:
        if hasattr(dep, 'x_studio_sitio') and dep.x_studio_sitio and not dep.sitio:
            sitio = env['tyt_studio.site'].browse(dep.x_studio_sitio.id)
            if sitio:
                dep.sitio = dep.x_studio_sitio.id
                update_department_len += 1
            else:
                _logger.warning(f"En el departmento {dep} no se podido actualizar el campo sitio, ya no existe el x_studio_sitio_id {dep.x_studio_sitio.id} en tyt_studio_site")
            
    _logger.info(f"Updated {update_department_len} departments")
    
    employees = env['hr.employee'].sudo().search([])
    update_employee_len = 0
    for emp in employees:
        if hasattr(emp, 'x_studio_sitio') and emp.x_studio_sitio and not emp.sitio:
            sitio = env['tyt_studio.site'].browse(emp.x_studio_sitio.id)
            if sitio:
                emp.sitio = emp.x_studio_sitio.id
                update_employee_len += 1
            else:
                _logger.warning(f"En el empleado {emp} no se podido actualizar el campo sitio, ya no existe el x_studio_sitio_id {emp.x_studio_sitio.id} en tyt_studio.site")
            
        if hasattr(emp, 'x_studio_numero') and emp.x_studio_numero and not emp.numero:
            emp.numero = emp.x_studio_numero 
            update_employee_len += 1
            
        if hasattr(emp, 'x_studio_sitios0') and emp.x_studio_sitios0 and not emp.sitios0:
            sitios0 = env['tyt_studio.sites'].browse(emp.x_studio_sitios0.id)
            if sitios0:
                emp.sitios0 = emp.x_studio_sitios0.id 
                update_employee_len += 1
            else:
                _logger.warning(f"En el empleado {us} no se podido actualizar el campo sitios0, ya no existe el x_studio_sitio_id {emp.x_studio_sitios0.id} en tyt_studio.sites")
            
    _logger.info(f"Updated {update_employee_len/3} employees")
            
    groups = env['res.groups'].sudo().search([])
    update_group_len = 0
    for group in groups:
        if hasattr(group, 'x_studio_job') and group.x_studio_job and not group.job_id:
            group.job_id = group.x_studio_job
            update_group_len += 1
            
    _logger.info(f"Update {update_group_len} groups")
            
    partners = env['res.partner'].sudo().search([])
    update_partner_len = 0
    for partner in partners:
        if hasattr(partner, 'x_studio_empleado') and partner.x_studio_empleado and not partner.empleado:
            partner.empleado = partner.x_studio_empleado
            update_partner_len += 1
        if hasattr(partner, 'x_studio_usuario') and partner.x_studio_usuario and not partner.usuario:
            partner.usuario = partner.x_studio_usuario
            update_partner_len += 1
         
    _logger.info(f"updated {update_partner_len/2} partners")
    jobs = env['hr.job'].sudo().search([])
    update_job_len = 0
    for job in jobs:
        if hasattr(job, 'x_studio_nesp') and job.x_studio_nesp and not job.nesp:
            job.nesp = job.x_studio_nesp
            update_job_len += 1
            
    _logger.info(f"Updated {update_job_len} jobs")
               
    
    env.cr.commit()