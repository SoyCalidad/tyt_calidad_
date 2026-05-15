/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

import { MaturityBarChart } from "./maturity_bar_chart";

export class MaturityLevelCard extends Component {

    static template = "tyt_risk_management.MaturityLevelCard";

    static components = {
        MaturityBarChart,
    };

    setup() {

        this.state = useState({
            collapsed: false,
        });

        this.mitigationData = {
            labels: [
                "No existe",
                "Inicial",
                "Limitado",
                "Definido",
                "Optimizado",
            ],

            data: [12, 28, 40, 18, 8],

            colors: [
                "#C10808",
                "#FC8C0E",
                "#FFC107",
                "#16AAFF",
                "#70C24A",
            ],
        };

        this.monitoringData = {
            labels: [
                "Inicial",
                "Básico",
                "Intermedio",
                "Avanzado",
                "Optimizado",
            ],

            data: [8, 14, 35, 27, 12],

            colors: [
                "#ef4444",
                "#f97316",
                "#facc15",
                "#22c55e",
                "#2563eb",
            ],
        };
    }

    toggleCollapse() {
        this.state.collapsed = !this.state.collapsed;
    }
}