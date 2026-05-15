/** @odoo-module **/

import { Component } from "@odoo/owl";
import { RiskQuadrant } from "./risk_quadrant";
export class RiskMap extends Component {
    static template = "tyt_risk_management.RiskMap";

    static props = {
        title : {
            type: String,
            optional: true,
        },//"Mapa de riesgos (Mitigación)",
    }
    static defaultProps = {
        title: "Mapa de riesgos",
    };

    static components = {
        RiskQuadrant,
    }

    setup() {
        this.rows = [
            {
                impact: "Alto",
                impactClass: "bg-danger-subtle",
                quadrants: [
                    {
                        id: 4,
                        className: "risk-yellow-1",
                        risks: [],
                    },
                    {
                        id: 7,
                        className: "risk-yellow-2",
                        risks: [],
                    },
                    {
                        id: 9,
                        className: "risk-red",
                        risks: [
                            { id: 34 },
                            { id: 29 },
                        ],
                    },
                ],
            },
            {
                impact: "Medio",
                impactClass: "bg-warning-subtle",
                quadrants: [
                    {
                        id: 2,
                        className: "risk-green",
                        risks: [],
                    },
                    {
                        id: 5,
                        className: "risk-yellow-1",
                        risks: [],
                    },
                    {
                        id: 8,
                        className: "risk-yellow-2",
                        risks: [
                            { id: 33 },
                            { id: 27 },
                            { id: 1 },
                        ],
                    },
                ],
            },
            {
                impact: "Bajo",
                impactClass: "bg-warning-light",
                quadrants: [
                    {
                        id: 1,
                        className: "risk-green",
                        risks: [],
                    },
                    {
                        id: 3,
                        className: "risk-green",
                        risks: [],
                    },
                    {
                        id: 6,
                        className: "risk-yellow-1",
                        risks: [
                            { id: 36 },
                            { id: 35 },
                            { id: 31 },
                            { id: 30 },
                            { id: 28 },
                            { id: 26 },
                            { id: 25 },
                        ],
                    },
                ],
            },
        ];

        this.occurrenceLevels = [
            {
                label: "Bajo",
                class: "bg-warning-light",
            },
            {
                label: "Medio",
                class: "bg-warning-subtle",
            },
            {
                label: "Alto",
                class: "bg-danger-subtle",
            },
        ];
    }

    get maxRiskCount() {
        return Math.max(
            ...this.rows.flatMap((row) =>
                row.quadrants.map((q) => q.risks.length)
            )
        );
    }

    get matrixSize() {
        return Math.ceil(Math.sqrt(this.maxRiskCount || 1));
    }
}