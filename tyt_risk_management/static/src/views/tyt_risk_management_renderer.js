import { ListRenderer } from "@web/views/list/list_renderer";
import { useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { RiskMap } from "./risk_map/risk_map";
export class RiskQuantificationListRenderer extends ListRenderer {
    static template = "tyt_risk_management.RiskQuantificationListRenderer";
    static components = {
        ...ListRenderer.components,
        RiskMap,
    };

    setup() {
        super.setup()

        console.log("this.props.props.list.records", this.props.list.records);

        this.orm = useService("orm");
        this.riskIds = this.props.list.records.map(risk => risk.data.id);
        this.mitigations = useState({
            "list": [],
            loading: true,
        })
        onWillStart(async () => {
            this.loadDataMitigations()
        })
    }



    async loadDataMitigations() {
        try {
            this.mitigations.loading = true;
            const data = await this.orm.call(
                "tyt.risk.mitigation",     
                "load_mitigation_from_risks", 
                [
                    this.riskIds,
                ]
            );
            this.mitigations.list = data
        } catch (error) {
            console.error("error al cargar mitigación ", error)
        } finally {
            setTimeout(() => {
                this.mitigations.loading = false;
                
            }, 50);

        }
    }


    openRecord(record) {
        // Reutiliza el mecanismo nativo del ListRenderer
        this.props.openRecord(record);
    }


}
