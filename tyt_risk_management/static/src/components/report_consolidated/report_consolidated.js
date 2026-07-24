/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { loadBundle } from "@web/core/assets";
import { Layout } from "@web/search/layout";
import { loadJS } from "@web/core/assets";

import { FilterSelect } from "./filter_select";
import { RiskSectionCard } from "./risk_section_card";
import { MaturityLevelCard } from "./maturity_level_card/maturity_level_card";
import { RiskMap } from "./risk_map/risk_map"
import { ProcessCard } from "./process_card/process_card";
import { MONTHS } from "./../utils";

export class ReportConsolidated extends Component {

    static template = "tyt_risk_management.ReportConsolidated";

    static components = {
        FilterSelect,
        Layout,
        RiskSectionCard,
        MaturityLevelCard,
        RiskMap ,
        ProcessCard,
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

            collapsedMitigation: false,
            collapsedMonitoring: false,

            loading: false,

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
                },
                processes_mitigated: [],
                processes_monitoring:[],
            },


        });

        this.monthOptions = MONTHS.map(m => ({value: m.id, label: m.name, ...m}));

        onWillStart(async () => {
            await this.loadInitialData();
            await loadJS("/tyt_risk_management/static/lib/echarts/echarts.min.js");
            await loadBundle("web.chartjs_lib");

            this.onSearch()
        });
    }

    async loadInitialData() {

        const deparments = await this.orm.searchRead(
            "hr.department",
            [['x_studio_npp', '=', 1]],
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
        if (availableYears) {
            this.state.filters.year = availableYears[0];
        }
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
        if (this.state.filters.pdomain_id && this.state.filters.pdomain_id!='0') {
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

        try {
            this.state.loading = true;
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
            setTimeout(() => {
                this.state.dataProcessed.barchart_mitigated = data.barchart_mitigated;
                this.state.dataProcessed.mitigated_riesgo_asegurado = data.mitigated_riesgo_asegurado;
                this.state.dataProcessed.monitoring_riesgo_asegurado = data.monitoring_riesgo_asegurado;
                this.state.dataProcessed.mitigated_riesgo_residual = data.mitigated_riesgo_residual;
                this.state.dataProcessed.monitoring_riesgo_residual = data.monitoring_riesgo_residual;
                this.state.dataProcessed.barchart_monitoring = data.barchart_monitoring;
                this.state.dataProcessed.maturity_mitigated = data.maturity_mitigated;
                this.state.dataProcessed.maturity_monitoring = data.maturity_monitoring;
                this.state.dataProcessed.resumenProcesos = data.resumenProcesos;
                this.state.dataProcessed.processes_mitigated = data.processes_mitigated;
                this.state.dataProcessed.processes_monitoring = data.processes_monitoring;
                console.log("state.dataProcessed", this.state.dataProcessed);
                console.log("state.dataProcessed.resumenProcesos", this.state.dataProcessed.resumenProcesos);
            this.state.loading = false;
                
            }, 50);

        } catch (error) {
            console.error("Error cargando procesos:", error);
            this.state.loading = false;

        } finally{
            // this.state.loading = false;
        }
    }

    toggleCollapseMitigation() {
        this.state.collapsedMitigation = !this.state.collapsedMitigation;
    }
    toggleCollapseMonitoring() {
        this.state.collapsedMonitoring = !this.state.collapsedMonitoring;
    }
}

registry.category("actions").add("tyt_risk_management.report_consolidated", ReportConsolidated);

