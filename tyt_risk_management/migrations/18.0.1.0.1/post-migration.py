from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Controles que el revisor ya marcó como mitigados pero que quedaron
    en 'En revisión' / 'Monitoreo' esperando a un auditor que no existe.
    Pasan a 'Mitigado' y recuperan su actividad anterior a la fase del auditor."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    stuck = env['tyt.risk.mitigation'].with_context(active_test=False).search([
        ('status', '=', 'under_review'),
        ('mr_status_mitigation', '=', 'mitigated'),
        ('risk_id_auditor_id', '=', False),
    ])
    if not stuck:
        return
    # Actividad previa: con planes de acción del revisor 'action_plan', si no 'mitigation'
    with_plans = stuck.filtered('mr_action_plan_ids')
    without_plans = stuck - with_plans
    # SQL directo para no disparar los correos de write()
    for records, activity in ((with_plans, 'action_plan'), (without_plans, 'mitigation')):
        if records:
            cr.execute(
                "UPDATE tyt_risk_mitigation SET status = 'mitigated', risk_activity_state = %s WHERE id IN %s",
                (activity, tuple(records.ids)),
            )
    stuck.invalidate_recordset(['status', 'risk_activity_state'])
    stuck.modified(['status', 'risk_activity_state'])
    env.flush_all()
