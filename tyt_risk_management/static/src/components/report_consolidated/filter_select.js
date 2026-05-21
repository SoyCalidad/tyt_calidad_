/** @odoo-module **/

import { Component } from "@odoo/owl";

export class FilterSelect extends Component {
    static template = "my_module.FilterSelect";

    static props = {
        label: String,
        name: String,
        value: {
            type: String,
            optional: true,
        },
        options: Array,
        placeholder: {
            type: String,
            optional: true,
        },
        mainClass: {
            type: String,
            optional: true,
        },
        onChange: {
            type: Function,
            optional: true,
        },
    };

    onChange(ev) {
        if (this.props.onChange) {
            this.props.onChange(this.props.name, ev.target.value);
        }
    }
}