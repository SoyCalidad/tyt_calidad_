/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";


export class ReviewerGuide extends Component {
    static template = "tyt_risk_management.ReviewerGuide";

    setup() {
        this.dialog = useService("dialog");
    
        // this.dialog.add(Dialog, {
        //     title: "Mi modal",
        //     body: "Contenido aquí",
        // });

    }
}

registry.category("actions").add("tyt_risk_management.reviewer_guide", ReviewerGuide);