/** @odoo-module **/

import { Component } from "@odoo/owl";

export class StatInfoCard extends Component {
    static template = "tyt_risk_management.StatInfoCard";

    static props = {
        title: String,
        value: String,
        color: String,
        icon: String,
    };
}