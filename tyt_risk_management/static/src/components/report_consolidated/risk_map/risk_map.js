/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { RiskQuadrant } from "./risk_quadrant";
import { MitigationDetail } from "./mitigation_detail";
export class RiskMap extends Component {
    static template = "tyt_risk_management.RiskMap";

    static props = {
        title : {
            type: String,
            optional: true,
        },//"Mapa de riesgos (Mitigación)",
        mitigations: {
            type: Array,
            optional: true,
        }
    }
    static defaultProps = {
        title: "Mapa de riesgos",
        mitigations: [],
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
                        ],
                    },
                ],
            },
        ];

        this.props.mitigations.forEach(mitigation => {
            if (mitigation.risk_id_quadrant > 0 && mitigation.risk_id_quadrant < 10) {
                this.rows.forEach(row  => {
                    row.quadrants.forEach(quadrant => {
                        if (quadrant.id == mitigation.risk_id_quadrant) {
                            quadrant.risks.push({
                                id: mitigation.risk_id_id,
                                idMitigation: mitigation.id,
                            })
                        }
                    })
                });
            }
        });

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

        this.state = useState({
            collapsed: false,
        });
    }

    toggleCollapse() {
        this.state.collapsed = !this.state.collapsed;
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