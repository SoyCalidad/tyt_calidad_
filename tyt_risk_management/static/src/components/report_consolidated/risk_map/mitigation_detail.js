/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";

export class MitigationDetail extends Component {
    /**
     * Mitigation Detail fo Risk Map
     */
    static template = "tyt_risk_management.RMMitigationDetail";

    static components = {Dialog};

    static props = {
        close: Function,
        idMitigation: Number,
        title: {
            type: String,
            optional: true,
        },
    };

    static defaultProps = {
        title: "DETALLE "
    }

    setup() {
        this.orm = useService("orm");

        this.state = useState({
            loading: false,
        });
        this.risk = useState({})

        onWillStart(async () => {
            this.loadMitigations();
        });
    }

    async execButton(callback) {
        if (this.isProcess) {
            return;
        }
        if (callback) {
            let shouldClose;
            try {
                shouldClose = await callback();
            } catch (e) {
                this.props.close();
                throw e;
            }
            if (shouldClose === false) {
                return;
            }
        }
        this.props.close();
    }

     async _cancel() {
        return this.execButton(this.props.cancel);
    }

    async loadMitigations() {
        this.state.loading = true;

        this.risk = await this.orm.call(
            "tyt.risk.mitigation",
            "mitigation_detail",
            [[this.props.idMitigation]],
        );

        this.state.loading = false;
    }

    get impactBadgeClass() {
        const impact = this.risk && this.risk.risk_impact;
        const colors = {
            Bajo: "bg-success",
            Medio: "bg-warning",
            Alto: "bg-danger",
        };
        return colors[impact] || "bg-secondary";
    }

    get occurenceBadgeClass() {
        const impact = this.risk && this.risk.risk_occurrence;
        const colors = {
            Bajo: "bg-success",
            Medio: "bg-warning",
            Alto: "bg-danger",
        };
        return colors[impact] || "bg-secondary";
    }


}