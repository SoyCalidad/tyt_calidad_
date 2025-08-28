/** @odoo-module **/

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { patch } from "@web/core/utils/patch";

patch(KanbanRenderer.prototype, {
    /**
     * Sobrescribimos _setState para añadir opciones de drag & drop
     */
    _setState(state) {
        super._setState(state);

        const arch = this.props.arch;
        if (arch.attrs.disable_drag_drop_record === "true") {
            this.columnOptions.draggable = false;
        }

        this.recordOptions.sortable = !(arch.attrs.disable_sort_record === "true");
        this.columnOptions.sortable = !(arch.attrs.disable_sort_column === "true");
    },

    /**
     * Sobrescribimos _renderGrouped para manejar la desactivación
     */
    _renderGrouped(fragment) {
        const res = super._renderGrouped(fragment);

        if (this.columnOptions.sortable === false && this.el) {
            // ⚠️ En OWL no existe this.$el.sortable, así que tendrías que
            // integrar una librería como SortableJS si necesitas esto.
            // Ejemplo (si usas SortableJS):
            // Sortable.get(this.el)?.option("disabled", true);
        }

        return res;
    },
});
