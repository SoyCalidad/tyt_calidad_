/** @odoo-module **/

import { Component } from "@odoo/owl";
import { MitigationDetail } from "./mitigation_detail";
import { useService } from "@web/core/utils/hooks";

export class RiskQuadrant extends Component {
    static template = "tyt_risk_management.RiskQuadrant";

    static props = {
        risks: Array,
        size: Number,
        className: String,
    }

    setup() {
        this.dialog = useService("dialog");
    }

    get matrix() {
        const size = this.props.size;
        const totalCells = size * size;

        const cells = [...this.props.risks];

        while (cells.length < totalCells) {
            cells.push(null);
        }

        const rows = [];

        for (let i = 0; i < totalCells; i += size) {
            rows.push(cells.slice(i, i + size));
        }
        console.log("matriz," , rows)
        return rows;
    }

    async onRiskClick(risk) {
        console.log("Risk selected:", risk);
        await this.dialog.add(MitigationDetail, {
            title: "DETALLE",
            idMitigation: risk?.idMitigation || 0,
        });
    }
}