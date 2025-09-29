/** @odoo-module **/

import { registry } from "@web/core/registry";
import { jsonrpc } from "@web/core/network/rpc_service";

function setupMarkAsRead() {
    document.body.addEventListener("click", async (ev) => {
        const target = ev.target.closest(".mark-as-read");
        if (!target) {
            return;
        }
        const messageId = target.dataset.id;
        if (messageId) {
            const result = await jsonrpc("/mark_as_read", {
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
        }
    });
}

// Registrar como "startup" para que se ejecute al cargar la web
registry.category("web_tour.startup").add("tyt_intranet_messaging.mark_as_read", {
    start() {
        setupMarkAsRead();
    },
});
