/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class CollapsibleCard extends Component {
    static template = "tyt_risk_management.CollapsibleCard";

    static props = {
        title: String,
        collapsed: {
            type: Boolean,
            optional: true,
            default: false,
        },
         slots: {
            type: Object,
            optional: true,
        },
         headerClass: {
            type: String,
            optional: true,
        },
    };

    setup() {
        this.state = useState({
            collapsed: this.props.collapsed || false,
        });
    }

    toggle() {
        this.state.collapsed = !this.state.collapsed;
    }
}