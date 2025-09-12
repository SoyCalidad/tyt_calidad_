/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { Component, onMounted } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";


class OrganizationalDashboard extends Component {

    static template = "hr_organizational_chart.organization_dashboard";

    setup() {
        onMounted(async () => {
            this.renderEmployeeDetails();
        })

    }

    async renderEmployeeDetails() {
        try {
            const result = await rpc("/get/parent/employee", {});
            this.parent_len = result[1]

            const childResponse = await rpc("/get/parent/child", {
                employee_id: result[0],
            } )
            const parentEl = document.querySelector("#o_parent_employee");
            if (parentEl && childResponse.html) {
                parentEl.insertAdjacentHTML("beforeend", childResponse.html);
                this._addEvents(parentEl, false);
                // parentEl.querySelectorAll(".employee_name").forEach(img => {
                //     img.addEventListener("click", (ev) => this.view_employee(ev));
                // });
                // parentEl.querySelectorAll("img").forEach(img => {
                //     img.addEventListener("click", (ev) => this._getChild_data(ev));
                // });
            }
        } catch (error) {
            console.error("Error en renderEmployeeDetails:", error);
        }
    }

    _addEvents(el, removeEventListener=true) {
        el.querySelectorAll(".employee_name").forEach(query => {

            query.addEventListener("click", (ev) => this.view_employee(ev))
        });
        el.querySelectorAll("img").forEach(img => {

            img.addEventListener("click", this._getChild_data.bind(this));
        });
    }

    // Evento: expandir/colapsar hijos
    async _getChild_data(ev) {
        const target = ev.target;
        console.log("target", target)
        if (target.parentElement?.className) {
            this.id = target.parentElement.id;
            this.check_child = document.querySelector(`#${CSS.escape(this.id)}.o_level_1`);

            if (this.check_child) {
                this.colspan_td = this.check_child.closest("td");
                this.tbody_child = this.colspan_td.closest("tbody");
                const child_length = this.tbody_child.children.length;

                if (child_length === 1) {
                    try {
                        const col_val = await rpc("/get/parent/colspan", {
                            emp_id: parseInt(this.id),
                        });
                        if (col_val) {
                            this.colspan_td.colSpan = col_val;
                        }

                        const result = await rpc("/get/child/data", {
                            click_id: parseInt(this.id),
                        });
                        console.log("tbody_child",this.tbody_child.querySelector("table:last-of-type"))
                        if (result) {
                            this.tbody_child.insertAdjacentHTML("beforeend", result);
                            this._addEvents(this.tbody_child.querySelector("table:last-of-type"));
                        }
                    } catch (error) {
                        console.error("Error en _getChild_data:", error);
                    }
                } else {
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
            this.env.services.action.doAction({
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
registry.category("actions").add("organization_dashboard", OrganizationalDashboard);
