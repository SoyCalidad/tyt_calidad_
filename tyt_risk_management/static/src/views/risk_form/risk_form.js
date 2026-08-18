/** @odoo-module **/

import { registry } from "@web/core/registry";
import { createElement, append } from "@web/core/utils/xml";
import { Notebook } from "@web/core/notebook/notebook";
import { formView } from "@web/views/form/form_view";
import { FormController } from '@web/views/form/form_controller';
import { useService } from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";
import { ReviewerGuide } from "../../components/reviewer_guide/reviewer_guide" 

import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

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

    async _saveBeforeNavigation() {
        const record = this.model.root;

        const dirty = await record.isDirty();

        if (!dirty) {
            return true;
        }

        const saved = await this.save({
            reload: false,
            onError: this.onSaveError.bind(this),
        });

        return saved !== false;
    }

    async beforeLeave() {
        const record = this.model.root;

        const saved = await this._saveBeforeNavigation();

        if (!saved) {
            return false;
        }
        console.log("record", record)
        if (
            record.data.mr_all_action_plans_complete &&
            record.data.mr_status_mitigation  !== "mitigated" &&
            record.data.is_reviewer
        ) {
            this.dialogService.add(ConfirmationDialog, {
                title: _t("Actualización requerida - Revisor"),
                body: _t(
                    "Todos los planes de acción han sido completados. " +
                    "Debe cambiar el estado del control a " +
                    "\"Mitigado\" antes de continuar."
                ),
                confirmLabel: _t("Aceptar"),
                confirm: () => {},
            });

            return false;
        }

        if (
            record.data.ma_all_action_plans_complete &&
            record.data.ma_status_mitigation  !== "mitigated" && 
            record.data.is_auditor && 
            record.data.mr_mitigation_status == 'mitigated'
        ) {
            this.dialogService.add(ConfirmationDialog, {
                title: _t("Actualización requerida - Auditor"),
                body: _t(
                    "Todos los planes de acción han sido completados. " +
                    "Debe cambiar el estado del control a " +
                    "\"Mitigado\" antes de continuar."
                ),
                confirmLabel: _t("Aceptar"),
                confirm: () => {},
            });

            return false;
        }

        return super.beforeLeave(...arguments);
    }

    async onPagerUpdate({ offset, resIds }) {
        const saved = await this._saveBeforeNavigation();

        if (!saved) {
            return false;
        }
        const record = this.model.root;

        if (
            record.data.mr_all_action_plans_complete &&
            record.data.mr_status_mitigation  !== "mitigated" &&
            record.data.is_reviewer 
        ) {
            this.dialogService.add(ConfirmationDialog, {
                title: _t("Actualización requerida - Revisor"),
                body: _t(
                    "Todos los planes de acción han sido completados. " +
                    "Debe cambiar el estado del control a \"Mitigado\" " +
                    "antes de cambiar de registro."
                ),
                confirmLabel: _t("Aceptar"),
                confirm: () => {},
            });

            return;
        }

        if (
            record.data.ma_all_action_plans_complete &&
            record.data.ma_status_mitigation  !== "mitigated" && 
            record.data.is_auditor && 
            record.data.mr_status_mitigation == 'mitigated'
        ) {
            this.dialogService.add(ConfirmationDialog, {
                title: _t("Actualización requerida - Auditor"),
                body: _t(
                    "Todos los planes de acción han sido completados. " +
                    "Debe cambiar el estado del control a " +
                    "\"Mitigado\" antes de continuar."
                ),
                confirmLabel: _t("Aceptar"),
                confirm: () => {},
            });

            return false;
        }

        return super.onPagerUpdate({ offset, resIds });
    }

    
}

 
export const RiskManagementFormView = {
    ...formView, 
    Controller: RiskFormController,
};

registry.category("views").add("risk_form", RiskManagementFormView);
