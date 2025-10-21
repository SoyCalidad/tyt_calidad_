/** @odoo-module **/

import { registry } from "@web/core/registry";
import { jsonRpc } from "@web/core/network/rpc";

import { Component, useState } from "@odoo/owl";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.tytIntranetMessaging = publicWidget.Widget.extend({
    selector: '.o_list_table',
    events: {
        'click a.mark-as-read': '_mark_as_read',
    },

    _mark_as_read: async function (ev) {

        // const target = ev.target.closest(".mark-as-read");
        const target = ev.currentTarget;
        if (!target) {
            return;
        }

        const messageId = target.dataset.id;
        if (!messageId) {
            return;
        }

        try {
            // const result = await jsonRpc("/mark_as_read", {
            //     message_id: messageId,
            // });

            const response = await fetch("/mark_as_read", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    jsonrpc: "2.0",
                    method: "call",
                    params: { message_id: messageId },
                    id: Math.floor(Math.random() * 1000),
                }),
            });
            const result = await response.json();

            if (result && result.result && result.result.success) {
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
    },


})
