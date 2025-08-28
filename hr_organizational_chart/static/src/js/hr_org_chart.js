/** @odoo-module **/
import { Component, onWillStart, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
// Si cargabas librerías externas antes con ajax.loadLibs:
import { loadJS, loadCSS } from "@web/core/assets";

export class OrgChartDepartment extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.action = useService("action");
        this.employee_data = [];
        this.href = window.location.href;

        onWillStart(async () => {
            // Carga opcional de librerías estáticas si las tenías en 16.0
            // await Promise.all([
            //     loadJS("/hr_org_chart_employee/static/lib/milib.js"),
            //     loadCSS("/hr_org_chart_employee/static/lib/milib.css"),
            // ]);

            // En 16 leías context.tag; en 18 el tag viene en props.action
            if (this.props?.action?.tag === "employee_organization_chart") {
                // Antes: this._rpc({route: "/get/employees"})
                const result = await this.rpc("/get/employees", {});

                // Antes: this._rpc({model, method, args})
                const values = await this.rpc("/web/dataset/call_kw", {
                    model: "hr.organizational.chart",
                    method: "get_employee_data",
                    args: [result],
                    kwargs: {},
                });
                this.employee_data = values || [];
            }
        });

        onMounted(() => {
            // Si quieres ocultar el control panel como hacías antes:
            document.querySelector(".o_control_panel")?.classList.add("o_hidden");
        });
    }

    async viewEmployee(ev) {
        // Usa dataset para evitar depender de índices de atributos
        const id = parseInt(ev.currentTarget?.dataset?.empId || ev.target?.dataset?.empId);
        if (!isNaN(id)) {
            await this.action.doAction({
                name: this.env._t("Employee"),
                type: "ir.actions.act_window",
                res_model: "hr.employee",
                res_id: id,
                views: [[false, "form"]],
                view_mode: "form",
            });
        }
    }
}

OrgChartDepartment.template = "hr_org_chart_employee.OrgChartDepartment";

// Registra el client action (reemplaza core.action_registry.add)
registry.category("actions").add("employee_organization_chart", OrgChartDepartment);

export default OrgChartDepartment;
