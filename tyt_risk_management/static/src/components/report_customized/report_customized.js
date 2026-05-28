/** @odoo-module */

import { Component, useState, onWillStart, useRef  } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { SelectMenu } from "@web/core/select_menu/select_menu";

import { MONTHS } from "../utils";

export class CustomizedReport extends Component {
    static template = 'tyt_risk_management.CustomizedReport';

    static components = { 
        Layout, 
        SelectMenu,
    };

    setup() {

        this.orm = useService("orm");
        this.state = useState({
            filters: {
                departmentIds: "0",
                domainIds: "0",
                processIds: "0",
                selectedYears: [],
                selectedMonths: [],
            },

            //data filters 
            loading: false,
            processes: [],
            domains: [],
            months: MONTHS.map(m => ({...m, label: m.name, value: m.id})),
            years: [],
            departments: [],
        });

        this.reportData = useState({});

        this.dialog = useService("dialog");
        onWillStart(async () => {
            await this.loadFilters();
            
            await this.onSearch()
        });

        
 
    }

    onMonthSelect(item) {
        this.state.filters.selectedMonths = item
    }

    onYearSelect(item) {
        this.state.filters.selectedYears = item
    }

    onProcessSelect(item) {
        this.state.filters.processIds = item
    }

    onDomainSelect(item) {
        this.state.filters.domainIds = item
    }

    onDepartmentSelect(item) {
        this.state.filters.departmentIds = item
    }


    onChangeDomain() {
        this.cargarProcesos()
    }

    async loadFilters() {
        await this.loadDomains();
        await this.cargarProcesos();
        await this.loadDepartments();
        try {
            const availableYears = await this.orm.call(
                "tyt.risk.mitigation",
                "get_available_years",
                []
            );
            this.state.years = availableYears.map(year => ({label: year.toString(), value: year.toString()}));
        }  catch (error) {
            console.error("Error cargando domains:", error);
        }


    }
    async loadDepartments() {
        try {
            const data = await this.orm.searchRead(
                "hr.department",
                [['x_studio_npp', '=', 1]],
                ["id", "name",]
            );
            this.state.departments = data.map(d => ({label: d.name, value: d.id}));
        } catch (error) {
            console.error("Error cargando domains:", error);
        }
    }

    async loadDomains() {
        try {
            const data = await this.orm.searchRead(
                "tyt.business.process",
                [["level", "=", 1]],
                ["id", "name", "short_name"],
            );

            this.state.domains = data.map(d => ({label: d.name, value: d.id}));
        } catch (error) {
            console.error("Error cargando domains:", error);
        }
    }

    async cargarProcesos() {
        try {
            const domain = [["level", "=", "2"]];
            const domainValue = this.state.filters.domain_id;
            if (domainValue && domainValue!='0') {
                domain.push(["parent_id", "=", domainValue])
            }
            const data = await this.orm.searchRead(
                "tyt.business.process",
                domain,
                ["id", "name", "short_name"]);
            this.state.processes = data.map(process => ({label: process.name, value: process.id}));
        } catch (error) {
            console.error("Error cargando procesos:", error);
        }
    }



    async openMitigation(mIds = []) {
        console.log("mids", mIds);
        await this.dialog.add(MitigationModal, {
            title: "Lista de riesgos",
            mIds,
            actionId: this.idActionActivity,
        });
    }

    async onSearch() {
        this.state.loading = true;
        // try {
        //     const data = await this.orm.call(
        //         "tyt.business.process",     
        //         "data_status_report", 
        //         [
        //             this.state.filters.department_id,
        //             this.state.filters.domain_id,
        //             this.state.filters.process_id,
        //             this.state.filters.year,
        //             this.state.filters.month,
        //         ]
        //     );
        //     this.state.reportData = data;

        // } catch (error) {
        //     console.error("Error cargando procesos:", error);
        // }
        this.state.loading = false;
        setTimeout(() => {
        }, 500);
    }
}

registry.category("actions").add("tyt_risk_management.report_customized", CustomizedReport);
