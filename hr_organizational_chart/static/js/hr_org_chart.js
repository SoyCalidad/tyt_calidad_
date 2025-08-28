/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

// Variable global para los datos
let employee_data = [];

/**
 * Función que arma el template de un nodo
 */
const nodeTemplate = (data) => `
    <span class="office">${data.office}</span>
    <div class="title">${data.name}</div>
    <div class="content">${data.title}</div>
`;

/**
 * Componente OWL que reemplaza el AbstractAction
 */
export class OrgChartDepartment extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.rpc = useService("rpc");

        this.container = useRef("orgChartContainer");

        onWillStart(async () => {
            // Cargar librerías JS externas si necesitas
            await loadJS("/hr_org_chart_employee/static/lib/orgchart.js");

            // Obtener datos de empleados
            const result = await this.rpc("/get/employees", {});
            employee_data = await this.orm.call(
                "hr.organizational.chart",
                "get_employee_data",
                [result]
            );
        });
    }

    /**
     * Renderiza el organigrama (antes QWeb.render)
     */
    mounted() {
        const container = this.container.el;
        container.innerHTML = this.renderChart();
    }

    renderChart() {
        // Aquí reemplazas QWeb.render con tu propio HTML
        return `
            <div class="org-chart-wrapper">
                ${employee_data.map((emp) => `
                    <div class="node" data-id="${emp.id}">
                        ${nodeTemplate(emp)}
                    </div>
                `).join("")}
            </div>
        `;
    }

    /**
     * Abre el empleado al hacer click
     */
    async onClickEmployee(ev) {
        const target = ev.target.closest(".node");
        if (target && target.dataset.id) {
            const id = parseInt(target.dataset.id);
            this.action.doAction({
                name: "Employee",
                type: "ir.actions.act_window",
                res_model: "hr.employee",
                res_id: id,
                view_mode: "form",
                views: [[false, "form"]],
            });
        }
    }
}

/**
 * Template OWL para el componente
 */
OrgChartDepartment.template = "hr_organizational_chart.OrgChartDepartment";

OrgChartDepartment.props = {};

/**
 * Registro como acción disponible en Odoo
 */
registry.category("actions").add("employee_organization_chart", OrgChartDepartment);
