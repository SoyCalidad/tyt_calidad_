/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { AbstractAction } from "@web/webclient/actions/abstract_action";
import { jsonRpc } from "@web/core/network/rpc_service";

export class EmployeeOrganizationalChart extends AbstractAction {
    setup() {
        super.setup();
        this.renderEmployeeDetails();
    }

    // Renderiza los detalles del empleado inicial
    async renderEmployeeDetails() {
        try {
            const result = await jsonRpc("/get/parent/employee", "call", {});
            this.parent_len = result[1];

            // Usamos fetch en vez de $.ajax
            const response = await fetch("/get/parent/child", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(result[0]),
            });
            const value = await response.text();
            document.querySelector("#o_parent_employee").insertAdjacentHTML("beforeend", value);
        } catch (error) {
            console.error("Error en renderEmployeeDetails:", error);
        }
    }

    // Evento: expandir/colapsar hijos
    async _getChild_data(ev) {
        const target = ev.target;
        if (target.parentElement?.className) {
            this.id = target.parentElement.id;
            this.check_child = document.querySelector(`#${this.id}.o_level_1`);

            if (this.check_child) {
                this.colspan_td = this.check_child.closest("td");
                this.tbody_child = this.colspan_td.closest("tbody");
                const child_length = this.tbody_child.children.length;

                if (child_length === 1) {
                    try {
                        const col_val = await jsonRpc("/get/parent/colspan", "call", {
                            emp_id: parseInt(this.id),
                        });
                        if (col_val) {
                            this.colspan_td.colSpan = col_val;
                        }

                        const result = await jsonRpc("/get/child/data", "call", {
                            click_id: parseInt(this.id),
                        });
                        if (result) {
                            this.tbody_child.insertAdjacentHTML("beforeend", result);
                        }
                    } catch (error) {
                        console.error("Error en _getChild_data:", error);
                    }
                } else {
                    // Colapsar hijos
                    for (let i = 0; i < 3; i++) {
                        this.tbody_child.children[1].remove();
                    }
                    this.colspan_td.colSpan = 2;
                }
            }
        }
    }

    // Evento: abrir empleado
    view_employee(ev) {
        if (ev.target.parentElement?.className) {
            const id = parseInt(ev.target.parentElement.parentElement.children[0].id);
            this.doAction({
                name: _t("Employee"),
                type: "ir.actions.act_window",
                res_model: "hr.employee",
                res_id: id,
                view_mode: "form",
                views: [[false, "form"]],
            });
        }
    }
}

// Registro del action
registry.category("actions").add("organization_dashboard", EmployeeOrganizationalChart);
