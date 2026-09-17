/** @odoo-module **/

import { registry } from "@web/core/registry";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";

registry.category("actions").add(
    "tyt_risk_management.action_plan_attendance_dialog",
    async (env, action) => {
        const formView = (action.views || []).find(
            ([viewId, viewType]) => viewType === "form"
        );

        const viewId = formView ? formView[0] : false;

        env.services.dialog.add(FormViewDialog, {
            resModel: action.res_model,
            resId: action.res_id,
            viewId: viewId,
            context: action.context || {},
            title: action.name || "Plan de acción",
            mode: "edit",
        });
    }
);

registry.category("actions").add(
    "tyt_risk_management.action_plan_reviewed",
    async (env, action) => {
        env.services.notification.add(
            action.params?.message || "El plan de acción fue enviado a revisión.",
            {
                type: "success",
            }
        );

        await env.services.action.doAction("soft_reload");
    }
);