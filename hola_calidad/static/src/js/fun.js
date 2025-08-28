/** @odoo-module **/

import { registry } from "@web/core/registry";
import { FormButton } from "@web/views/form/form_button";

/**
 * Extendemos el comportamiento del FormButton
 */
export class CustomFormButton extends FormButton {
    async onClick(ev) {
        if (this.props.node.attrs.custom === "click") {
            console.log("CALL FUN FUNCTION");
            // alert("It works!!");
            return;
        }
        // Caso contrario se ejecuta el comportamiento normal
        await super.onClick(ev);
    }
}

// Reemplazar el componente original en el registry
registry.category("view_widgets").add("button", CustomFormButton);
