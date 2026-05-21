/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

import { MaturityBarChart } from "./maturity_bar_chart";

export class MaturityLevelCard extends Component {

    static template = "tyt_risk_management.MaturityLevelCard";

    static props = {
        dataMitigated: Array ,
        dataMonitoring: Array, // 5 element
    }

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

            data: this.props.dataMitigated,

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

            data: this.props.dataMonitoring,

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