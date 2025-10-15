/** @odoo-module **/

import { registry } from "@web/core/registry";
import { jsonRpc } from "@web/core/network/rpc";

function setupMarkAsRead() {
    document.body.addEventListener("click", async (ev) => {
        const target = ev.target.closest(".mark-as-read");
        if (!target) {
            return;
        }

        const messageId = target.dataset.id;
        if (!messageId) {
            return;
        }

        try {
            const result = await jsonRpc("/mark_as_read", {
                message_id: messageId,
            });

            if (result && result.success) {
                document.querySelectorAll(`[data-id="${messageId}"] span`).forEach(el => {
                    el.classList.remove("fw-bold");
                });
                document.querySelectorAll(`[data-id="${messageId}"]`).forEach(el => {
                    el.classList.remove("fw-bold");
                });
            }
        } catch (error) {
            console.error("Error en mark_as_read:", error);
        }
    });
}

// Registrar el código para que se ejecute al iniciar el cliente web
registry.category("web_tour.startup").add("tyt_intranet_messaging.mark_as_read", {
    start() {
        setupMarkAsRead();
    },
});
