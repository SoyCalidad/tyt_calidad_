/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { loadBundle } from "@web/core/assets";
import { Layout } from "@web/search/layout";

import { FilterSelect } from "./filter_select";
import { RiskSectionCard } from "./risk_section_card";
import { MaturityLevelCard } from "./maturity_level_card/maturity_level_card";
import { RiskMap } from "./risk_map/risk_map"

export class ReportConsolidated extends Component {

    static template = "tyt_risk_management.ReportConsolidated";

    static components = {
        FilterSelect,
        Layout,
        RiskSectionCard,
        MaturityLevelCard,
        RiskMap ,
    };

    setup() {

        this.orm = useService("orm");

        this.state = useState({
            filters: {
                deparment_id: "",
                dominio: "",
                proceso: "",
                year: "",
                month: "",
            },

            deparments: [],
            domains : [],
            processes: [],
            years: []
        });

        this.monthOptions = [
            { value: "0", label: "Todo" },
            { value: "1", label: "Enero" },
            { value: "2", label: "Febrero" },
            { value: "3", label: "Marzo" },
            { value: "4", label: "Abril" },
            { value: "5", label: "Mayo" },
            { value: "6", label: "Junio" },
            { value: "7", label: "Julio" },
            { value: "8", label: "Agosto" },
            { value: "9", label: "Septiembre" },
            { value: "10", label: "Octubre" },
            { value: "11", label: "Noviembre" },
            { value: "12", label: "Diciembre" },
        ];

        onWillStart(async () => {
            await this.loadInitialData();
            await loadBundle("web.chartjs_lib");

        });
    }

    async loadInitialData() {

        const deparments = await this.orm.searchRead(
            "hr.department",
            [],
            ["id", "name"]
        );
        this.state.deparments = deparments.map(c => ({
            value: c.id,
            label: c.name,
        }));

        const domains = await this.orm.searchRead(
            "tyt.business.process",
            [["level", "=", 1]],
            ["id", "name"],
        )

        this.state.domains = domains.map(c => ({
            value: c.id,
            label: c.name,
        }));

        const processes = await this.orm.searchRead(
            "tyt.business.process",
            [["level", "=", 2]],
            ["id", "name"],
        );

        this.state.processes = processes.map(c => ({
            value: c.id,
            label: c.name,
        }));

        

        const availableYears = await this.orm.call(
            "tyt.risk.mitigation",
            "get_available_years", 
            []
        );

        this.state.years = availableYears.map(c => ({
            value: c,
            label: c,
        }));;
    }

    updateFilter(name, value) {
        this.state.filters[name] = value;
    }

    async onSearch() {

        console.log("Filtros", this.state.filters);

        if (this.props.onSearch) {
            await this.props.onSearch(this.state.filters);
        }
    }
}

registry.category("actions").add("tyt_risk_management.report_consolidated", ReportConsolidated);

