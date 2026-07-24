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


    COLORS_CONTROLS = {
            'Insignificate': 'bg-secondary',
            'Menor': 'bg-success',
            'Mayor': 'bg-danger',
            'Significativo': 'bg-warning',
            'Severo': 'tyt-bg-darkred',
        }
    get beforeControlClass() {
        const beforeControl = this.risk && this.risk.before_control;

        return this.COLORS_CONTROLS[beforeControl] || "";
    }

    get afterControlClass() {
        const control = this.risk && this.risk.after_control;
        return this.COLORS_CONTROLS[control] || "";
    }

    COLORS_STATUS_MITIGATION = {
            'No Mitigado': 'bg-secondary',
            'Parcialmente Mitigado': 'bg-warning',
            'Mitigado': 'bg-success',
        }
    get mrStatusMitigationClass() {
        const mrStatusMitigation = this.risk && this.risk.mr_status_mitigation;
        return this.COLORS_STATUS_MITIGATION[mrStatusMitigation] || 'bg-secondary';
    }

    get maStatusMitigationClass() {
        const mrStatusMitigation = this.risk && this.risk.ma_status_mitigation;
        return this.COLORS_STATUS_MITIGATION[mrStatusMitigation] || 'bg-secondary';
    }

    COLORS_LEVEL_COMPLIANCE = {
        'No atendido': 'bg-danger',
        'Programado': 'bg-secondary',
    }

    get mrLevelComplianceClass() {
        const level = this.risk && this.risk.mr_level_compliance ;
        return this.COLORS_LEVEL_COMPLIANCE[level] || 'bg-secondary';

    }

    get maLevelComplianceClass() {
        const level = this.risk && this.risk.ma_level_compliance ;
        return this.COLORS_LEVEL_COMPLIANCE[level] || 'bg-secondary';

    }


}