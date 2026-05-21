/** @odoo-module **/

import { Component } from "@odoo/owl";

export class RiskQuadrant extends Component {
    static template = "tyt_risk_management.RiskQuadrant";

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
        console.log(rows)
        return rows;
    }

    onRiskClick(risk) {
        console.log("Risk selected:", risk);
    }
}