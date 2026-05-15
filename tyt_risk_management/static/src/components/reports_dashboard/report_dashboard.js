/** @odoo-module **/

import { Component , onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

export class ReportesDashboard extends Component {
    static components = { Layout };

    setup() {
        this.orm = this.env.services.orm;
        this.actionService = this.env.services.action;

        this.allReports = [
            { name: "Nivel 0 - Carga inicial", icon: "fa-upload", action: "tu_modulo.action_1" },
            { name: "Nivel 1 - Actividades", icon: "fa-line-chart", action: "tu_modulo.action_2" },
            { name: "Nivel 2 - Estatus", icon: "fa-info-circle", action: "tu_modulo.action_3" },
            { name: "Nivel 3 - Consolidado", icon: "fa-info-circle", action: "tu_modulo.action_3" },
            { name: "Nivel 4 - Personalizado", icon: "fa-info-circle", action: "tu_modulo.action_3" },
            { name: "Nivel 5 - Ejecutivo", icon: "fa-info-circle", action: "tu_modulo.action_3" },
            { name: "Nivel 6 - Planes de acción", icon: "fa-info-circle", action: "tu_modulo.action_3" },
            { name: "7.1 Desempeño de Evaluaciones Efectuadas", icon: "fa-info-circle", action: "tu_modulo.action_3" },
            { name: "7.2 Desempeño de Evaluaciones Efectuadas, Consolidado", icon: "fa-info-circle", action: "tu_modulo.action_3" },
            { name: "7.3 Desempeño de Acciones de Remediación", icon: "fa-info-circle", action: "tu_modulo.action_3" },
            { name: "7.4 Nivel de Apetito de Riesgo", icon: "fa-info-circle", action: "tu_modulo.action_3" },
            { name: "7.5 Calificación y Desempeño del Riesgo", icon: "fa-info-circle", action: "tu_modulo.action_3" },
            { name: "Nivel 8 - Certificación", icon: "fa-info-circle", action: "tu_modulo.action_3" },
        ];

        this.reports = [];

        onWillStart(async () => {
            this.reports = [];

            for (const r of this.allReports) {
                try {
                    // intenta cargar la acción
                    //await this.actionService.loadAction(r.action);
                    this.reports.push(r);
                } catch (e) {
                    // si falla → no tiene permisos → no mostrar
                }
            }
        });
    }

    openReport(action_xmlid) {
        this.env.services.action.doAction(action_xmlid);
    }
}

ReportesDashboard.template = "tyt_risk_management.report_dashboard";

registry.category("actions").add("tyt_risk_management.report_dashboard", ReportesDashboard);