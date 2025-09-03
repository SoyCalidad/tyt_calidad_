/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";

patch(ListController.prototype,  {

    // Eventos adicionales
    events: Object.assign({}, ListController.prototype.events, {
        "click .o_list_bug_report": "_onClickBugReport",
    }),

    /**
     * Acción al hacer click en el botón
     */
    _onClickBugReport(ev) {
        ev.preventDefault();
        this.env.services.action.doAction({
            type: "ir.actions.act_url",
            target: "new",
            url: "https://forms.gle/EjwLyPoFtcM5WojY8",
        });
    },
});
