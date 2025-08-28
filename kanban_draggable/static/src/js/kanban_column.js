/** @odoo-module **/

import { KanbanColumn } from "@web/views/kanban/kanban_column";
import { patch } from "@web/core/utils/patch";

patch(KanbanColumn.prototype,  {
    async start() {
        await super.start();

        if (this.props.recordOptions?.sortable === false) {
            // ⚠️ En OWL ya no existe this.$el.sortable
            // Debes usar SortableJS (que ya está integrado en Odoo)
            const sortable = Sortable.get(this.el);
            if (sortable) {
                sortable.option("disabled", true);
            }
        }
    },
});
