/** @odoo-module **/

import { registry } from "@web/core/registry";
import { createElement, append } from "@web/core/utils/xml";
import { Notebook } from "@web/core/notebook/notebook";
import { formView } from "@web/views/form/form_view";
import { FormController } from '@web/views/form/form_controller';
import { useService } from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";
import { ReviewerGuide } from "./../reviewer_guide/reviewer_guide" 


export class RiskFormController extends FormController {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
    }

    onClickInfo() {
        const record = this.model.root.data;

        

        this.dialog.add(ReviewerGuide, {
            info: "data",
        });
    }

    
}

 
export const RiskManagementFormView = {
    ...formView, 
    Controller: RiskFormController,
};

registry.category("views").add("risk_form", RiskManagementFormView);
