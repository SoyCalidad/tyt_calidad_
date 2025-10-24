import logging 

_logger = logging.getLogger(__name__)

def _format_query(query, not_ids):
    if not_ids:
        query += " WHERE id not in %s \n" % (tuple(not_ids),)
    query += " ON CONFLICT (id) DO NOTHING;"
    if ',)' in query:
        query = query.replace(',)',')')
    return query

def _format_query_set_val(table_name):
    return """
        SELECT setval(
            pg_get_serial_sequence('{0}', 'id'),
            (SELECT COALESCE(MAX(id), 1) FROM {0})
        );
    """.format(table_name)

def _migrate_models_with_sql(env):
    """
    Retrun True if all is correct
    """
    cr = env.cr 
    _logger.info("Init migrate models with sql")
    if 'x_area_encuesta' in env:
        try:
            _logger.info("Init x_area_encuesta migrations")
            
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_survey_area AS a
                WHERE a.id IN (SELECT id FROM x_area_encuesta)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_survey_area (id, name, active, code, sequence, create_date, write_date, create_uid, write_uid)
                SELECT id, x_name, x_active, x_studio_code, x_studio_sequence, create_date, write_date, create_uid, write_uid
                FROM x_area_encuesta
                
            """
            cr.execute(_format_query(query, exist_ids))
                

            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio.survey_area")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio.survey_area")
            cr.execute(_format_query_set_val('tyt_studio_survey_area'))
            cr.commit()
    
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_area_encuesta: {e}")
            return False
    
    if 'x_tipo_encuesta' in env:
        try:
            _logger.info("Init x_tipo_encuesta migrations")
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_survey_type AS a
                WHERE a.id IN (SELECT id FROM x_tipo_encuesta)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_survey_type (id, name, active, code, sequence, create_date, write_date, create_uid, write_uid)
                SELECT id, x_name, x_active, x_studio_code, x_studio_sequence, create_date, write_date, create_uid, write_uid
                FROM x_tipo_encuesta
                
            """
            cr.execute(_format_query(query, exist_ids))
            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio_survey_type")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_survey_type")
            cr.execute(_format_query_set_val('tyt_studio_survey_type'))
            cr.commit()
            
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_tipo_encuesta: {e}")
            return False
            
    if 'x_noms' in env:
        try:
            _logger.info("Init x_noms migrations")
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_noms AS a
                WHERE a.id IN (SELECT id FROM x_noms)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_noms (id, name, create_date, write_date, create_uid, write_uid)
                SELECT id, x_name, create_date, write_date, create_uid, write_uid
                FROM x_noms 

            """
            cr.execute(_format_query(query, exist_ids))
            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio_noms")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_noms")
            cr.execute(_format_query_set_val('tyt_studio_noms'))
            cr.commit()
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_noms: {e}")
            return False

    if 'x_tipo_sitio' in env:
        try:
            _logger.info("Init x_tipo_sitio migrations")
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_type_site AS a
                WHERE a.id IN (SELECT id FROM x_tipo_sitio)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_type_site (id, name, active, sequence, create_date, write_date, create_uid, write_uid)
                SELECT id, x_name, x_active, x_studio_sequence, create_date, write_date, create_uid, write_uid
                FROM x_tipo_sitio 

            """
            cr.execute(_format_query(query, exist_ids))
            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio_type_site")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_type_site")
            cr.execute(_format_query_set_val('tyt_studio_type_site'))
            cr.commit()
        
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_tipo_sitio: {e}")
            return False
            
    if 'x_sitios' in env:
        try:
            _logger.info("Init x_sitios migrations")
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_sites AS a
                WHERE a.id IN (SELECT id FROM x_sitios)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_sites (id, name, create_date, write_date, create_uid, write_uid)
                SELECT id, x_name, create_date, write_date, create_uid, write_uid
                FROM x_sitios 
            """
            cr.execute(_format_query(query, exist_ids))
            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio_sites")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_sites")
            cr.execute(_format_query_set_val('tyt_studio_sites'))
            cr.commit()
       
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_sitios: {e}") 
            return False

    if 'x_sitio' in env:
        _logger.info("Init x_sitio migrations")
        try:
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_site AS a
                WHERE a.id IN (SELECT id FROM x_sitio)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_site (id, active, name, codigo, cuan, cuenta_analitica, departamento, id0, "many2one_field_7AsCR", nombre2 , sequence, sitio1, sitios, sitios0, tipo_sitio, create_date, write_date, create_uid, write_uid)
                SELECT id, x_active, x_name, x_studio_codigo, x_studio_cuan, x_studio_cuenta_analitica, x_studio_departamento, x_studio_id0, x_studio_many2one_field_7AsCR, x_studio_nombre2, x_studio_sequence, x_studio_sitio1, x_studio_sitios, x_studio_sitios0, x_studio_tipo_sitio, create_date, write_date, create_uid, write_uid
                FROM x_sitio 
                
            """
            cr.execute(_format_query(query, exist_ids))
            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio_site")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_site")
            cr.execute(_format_query_set_val('tyt_studio_site'))
            cr.commit()

        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_sitio: {e}")
            return False

    if 'x_ano' in env:
        _logger.info("Init x_ano migrations")
        try:
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_ano AS a
                WHERE a.id IN (SELECT id FROM x_ano)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_ano (id, name, create_date, write_date, create_uid, write_uid)
                SELECT id, x_name, create_date, write_date, create_uid, write_uid
                FROM x_ano 
            
            """
            cr.execute(_format_query(query, exist_ids))
            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio_ano")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_ano")
            cr.execute(_format_query_set_val('tyt_studio_ano'))
            cr.commit()
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_ano: {e}")
            return False

    if 'x_gnnnn' in env:
        _logger.info("Init x_gnnnn migrations")
        try:
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_gnnnn AS a
                WHERE a.id IN (SELECT id FROM x_gnnnn)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_gnnnn (id, name, create_date, write_date, create_uid, write_uid)
                SELECT id, x_name, create_date, write_date, create_uid, write_uid
                FROM x_gnnnn 
            
            """
            cr.execute(_format_query(query, exist_ids))
            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio_gnnnn")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_gnnnn")
            cr.execute(_format_query_set_val('tyt_studio_gnnnn'))
            cr.commit()
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_gnnnn: {e}")
            return False

    if 'x_mes' in env:
        _logger.info("Init x_mes migrations")
        try:
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_mes AS a
                WHERE a.id IN (SELECT id FROM x_mes)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_mes (id, name, numero, create_date, write_date, create_uid, write_uid)
                SELECT id, x_name, x_studio_numero, create_date, write_date, create_uid, write_uid
                FROM x_mes 
            """
            cr.execute(_format_query(query, exist_ids))
            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio_mes")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_mes")
            cr.execute(_format_query_set_val('tyt_studio_mes'))
            cr.commit()
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_mes: {e}")
            return False
      

    if 'x_tipo_priodo' in env:
        _logger.info("Init x_tipo_priodo migrations")
        try:
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_period_type AS a
                WHERE a.id IN (SELECT id FROM x_tipo_priodo)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_period_type (id, name, code, create_date, write_date, create_uid, write_uid)
                SELECT id, x_name, x_studio_code, create_date, write_date, create_uid, write_uid
                FROM x_tipo_priodo 
            """
            cr.execute(_format_query(query, exist_ids))
            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio_period_type")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_period_type")
            cr.execute(_format_query_set_val('tyt_studio_period_type'))
            cr.commit()
            
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_tipo_priodo: {e}")
            return False


    if 'x_periodo' in env:
        _logger.info("Init x_periodo migrations")
        try:
            cr.execute("""
                SELECT a.id
                FROM tyt_studio_period AS a
                WHERE a.id IN (SELECT id FROM x_periodo)
            """)
            exist_ids = [r[0] for r in cr.fetchall()]
            query = """
                INSERT INTO tyt_studio_period (id, name, amc, ano, anoc, "asc", diaac, diac, diamc, diasc, f1, f2, g, gg, gnnnn, mes, mes0, mes00, mesac, mesc, mesm00, semana, semanac, tipo_periodo, tpid, create_date, write_date, create_uid, write_uid)
                SELECT id, x_name, x_studio_amc, x_studio_ano, x_studio_anoc, x_studio_asc, x_studio_diaac, x_studio_diac, x_studio_diamc, x_studio_diasc, x_studio_f1, x_studio_f2, x_studio_g, x_studio_gg, x_studio_gnnnn, x_studio_mes, x_studio_mes0, x_studio_mes00, x_studio_mesac, x_studio_mesc, x_studio_mesm00, x_studio_semana, x_studio_semanac, x_studio_tipo_periodo, x_studio_tpid, create_date, write_date, create_uid, write_uid
                FROM x_periodo 
            """
            cr.execute(_format_query(query, exist_ids))
            if exist_ids:
                _logger.warning(f"Ya existe los ids {exist_ids} en tyt_studio_period")
                
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_period")
            cr.execute(_format_query_set_val('tyt_studio_period'))
            cr.commit()
            
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar x_periodo: {e}")
            return False
    
    # many2many
    if 'x_x_noms_x_sitio_rel' in env:
        _logger.info("Init x_x_noms_x_sitio_rel migrations")
        try:
            query = """
                INSERT INTO tyt_studio_noms_tyt_studio_site_rel (tyt_studio_site_id, tyt_studio_noms_id)
                SELECT x_sitio_id, x_noms_id
                FROM x_x_noms_x_sitio_rel 
                ON CONFLICT DO NOTHING;
            """
            cr.execute(query)
            if cr.rowcount:
                _logger.info(f"Created {cr.rowcount} of tyt_studio_noms_tyt_studio_site_rel")
            cr.commit()
            
        except Exception as e:
            cr.rollback()
            _logger.error(f"Error al migrar tyt_studio_noms_tyt_studio_site_rel: {e}")
            return False
    
    try:
        #Inserta el campo site_id en sites 
        sitios = env['tyt_studio.sites'].sudo().search([], order='id asc')
        x_sitios = env['x_sitios'].sudo().search([], order='id asc')
        update_sites_len = 0
        for index, sitios0 in enumerate(sitios):
            if sitios0.id in x_sitios.ids:
                if not sitios0.site_id and hasattr(x_sitios[index], 'x_studio_sitio') and x_sitios[index].x_studio_sitio:
                    sitios0.site_id = x_sitios[index].x_studio_sitio
                    update_sites_len += 1
                    
                    
        cr.commit()
        _logger.info(f"Se actualizarón {update_sites_len} tyt_studio_sites(site_id)")
    
    except Exception as e:
        cr.rollback()
        _logger.error(f"Error al actualizar sites con site_id: {e}")
        return False

    
    return True
        
                
         
