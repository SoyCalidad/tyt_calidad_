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
                department_id: "0",
                pdomain_id: "0",
                process_id: "0",
                year: "0",
                month: "0",
            },

            //data filters
            deparments: [],
            domains : [],
            processes: [],
            years: [],

            //dataprocessed
            dataProcessed: {
                barchart_mitigated: [0,0,0],
                mitigated_riesgo_asegurado: 0,
                monitoring_riesgo_asegurado: 0,
                mitigated_riesgo_residual: 0,
                monitoring_riesgo_residual: 0,
                barchart_monitoring: [0,0,0],
                maturity_mitigated: [0,0,0,0,0],
                maturity_monitoring: [0,0,0,0,0],
                resumenProcesos: {
                    mitigado: [],
                    monitoring: [],
                }
            },


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
            await this.onSearch()
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

        await this._loadProcess()

        

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
        console.log("update filter", name, value);
        console.log("state filter", this.state.filters)
        if (name=='pdomain_id') {
            this._loadProcess();
        }
    }

 

    async _loadProcess() {
        const domain = [["level", "=", 2]];
        if (this.state.filters.pdomain_id) {
            domain.push(["parent_id", "=", Number(this.state.filters.pdomain_id)])
        }
        const processes = await this.orm.searchRead(
            "tyt.business.process",
            domain,
            ["id", "name"],
        );

        this.state.processes = processes.map(c => ({
            value: c.id,
            label: c.name,
        }));
    }

    async onSearch() {

        console.log("Filtros", this.state.filters);
        console.log("Esp", this.state.filters.department_id,
                    this.state.filters.pdomain_id,
                    this.state.filters.process_id,
                    this.state.filters.year,
                    this.state.filters.month,)

        try {
            const data = await this.orm.call(
                "tyt.risk.mitigation",     
                "report_consolidated", 
                [
                    this.state.filters.department_id,
                    this.state.filters.pdomain_id,
                    this.state.filters.process_id,
                    this.state.filters.year,
                    this.state.filters.month,
                ]
            );
            //this.state.processedData = data;
            this.state.dataProcessed = data;

        } catch (error) {
            console.error("Error cargando procesos:", error);
        }
    }
}

registry.category("actions").add("tyt_risk_management.report_consolidated", ReportConsolidated);

