/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";

export class RCMitigationModal extends Component {
    static template = "tyt_risk_management.RCMitigationModal";

    static components = {Dialog};

    static props = {
        close: Function,
        mIds: Array,
        title: String,
        "*": true,
    };

    setup() {
        this.orm = useService("orm");

        this.state = useState({
            mitigations: [],
            loading: true,
        });

        onWillStart(async () => {
            await this.loadMitigations();
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

        this.state.mitigations = await this.orm.read(
            "tyt.risk.mitigation",
            this.props.mIds,
            ["id","risk_id_auditor_id", "risk_id_reviewer_id", "risk_id_owner_id",  "risk_id_id", "risk_id_pdomain_id", "period_str", "year", "month", "risk_id_subprocess_id", "risk_id_process_id", "mr_degree_mitigation", "ma_degree_mitigation", ]
        );

        this.state.loading = false;
    }


    /**
     * 
     * @param {*} departmentId 
     * 
     */
    openDepartment(departmentId) {
        

        const url = `/odoo/action-${this.props.actionId}/${departmentId}`;

        window.open(url, "_blank");
    }
}