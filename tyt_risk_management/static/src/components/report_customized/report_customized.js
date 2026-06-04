/** @odoo-module */

import { Component, useState, onWillStart, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { SelectMenu } from "@web/core/select_menu/select_menu";

import { MitigationModal } from "./../report_status/mitigation_modal/mitigation_modal";

import { MONTHS } from "../utils";

export class CustomizedReport extends Component {
    static template = 'tyt_risk_management.CustomizedReport';

    static components = {
        Layout,
        SelectMenu,
    };

    setup() {

        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.state = useState({
            filters: {
                departmentIds: [],
                domainIds: [],
                processIds: [],
                selectedYears: [],
                selectedMonths: [],
            },

            //data filters 
            loading: false,
            processes: [],
            domains: [],
            months: MONTHS.map(m => ({ ...m, label: m.name, value: m.id })).sort((a, b) => a.id - b.id),
            years: [],
            departments: [],
        });
        console.log("meses", this.state.months)
        this.reportData = useState({});

        this.dialog = useService("dialog");
        onWillStart(async () => {
            await this.loadFilters();

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
            this.state.years = availableYears.map(year => ({ label: year.toString(), value: year.toString() }));
        } catch (error) {
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
            this.state.departments = data.map(d => ({ label: d.name, value: d.id }));
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

            this.state.domains = data.map(d => ({ label: d.name, value: d.id }));
        } catch (error) {
            console.error("Error cargando domains:", error);
        }
    }

    async cargarProcesos() {
        try {
            const domain = [["level", "=", "2"]];
            const domainValue = this.state.filters.domain_id;
            if (domainValue && domainValue != '0') {
                domain.push(["parent_id", "=", domainValue])
            }
            const data = await this.orm.searchRead(
                "tyt.business.process",
                domain,
                ["id", "name", "short_name"]);
            this.state.processes = data.map(process => ({ label: process.name, value: process.id }));
        } catch (error) {
            console.error("Error cargando procesos:", error);
        }
    }



    async openMitigation(mIds = []) {
        console.log("mids", mIds);
        if (!mIds) {
            return;
        }
        await this.dialog.add(MitigationModal, {
            title: "Lista de riesgos",
            mIds,
            actionId: this.idActionActivity,
            // showAction: false,
            // keysMitigation: ["id","risk_id_auditor_id", "risk_id_reviewer_id", "risk_id_owner_id",  "risk_id_id", "risk_id_pdomain_id", "period_str", "year", "month", "risk_id_subprocess_id", "risk_id_process_id", "mr_degree_mitigation", "ma_degree_mitigation", ],
            // labelTable: [
            //     {label: "ID Riesgo", key: "risk_id_id", is_m2o: false},
            //     {label: "Dominio", key: "risk_id_pdomain_id", is_m2o: true},
            //     {label: "Año", key: "year", is_m2o: false},
            //     {label: "Mes", key: "month", is_m2o: false},
            //     {label: "Proceso", key: "risk_id_process_id", is_m2o: true},
            //     {label: "Sub Proceso", key: "risk_id_subprocess_id", is_m2o: true},
            //     {label: "Estatus de mitigación", key: "mr_degree_mitigation", is_m2o: true},
            //     {label: "Dueño del proceso", key: "risk_id_owner_id", is_m2o: true},
            //     {label: "Dueño del control", key: "risk_id_owner_id", is_m2o: true},
            //     {label: "Revisor", key: "risk_id_reviewer_id", is_m2o: true,},
            //     {label: "Estatus de monitoreo", key: "ma_degree_mitigation", is_m2o: true},

            //     {label: "Auditor", key: "risk_id_auditor_id", is_m2o: true},
            // ]
        });
    }

    async onSearch() {
        this.state.loading = true;
        try {
            const data = await this.orm.call(
                "tyt.risk.mitigation",     
                "customized_report", 
                [
                    this.state.filters.departmentIds,
                    this.state.filters.domainIds,
                    this.state.filters.processIds,
                    this.state.filters.selectedYears,
                    this.state.filters.selectedMonths,
                ]
            );
            this.reportData = data;
            this.state.loading = false;

        } catch (error) {
            this.state.loading = false;
            this.notification.add(
                error.message || "No se pudo generar el reporte.",
                {
                    title: "Error",
                    type: "danger",
                }
            );
            console.error("Error onsearch:", error);
        }
        
        
    }

    async download() {
        try {
            this.state.loading = true;
            // Crear wizard
            const wizardId = await this.orm.create(
                "tyt.customized.report.wizard",
                [{
                    years: this.state.filters.selectedYears.toString() || "",
                    months: this.state.filters.selectedMonths.toString() || "",
                    department_ids: [[6,0, this.state.filters.departmentIds || []]],
                    pdomain_ids: [[6,0, this.state.filters.domainIds || []]],
                    process_ids: [[6,0, this.state.filters.processIds || []]],

                }]
            );

            // Ejecutar método que devuelve ir.actions.report
            const reportAction = await this.orm.call(
                "tyt.customized.report.wizard",
                "action_generate_xlsx",
                [[wizardId]]
            );

            // Lanzar descarga
            await this.action.doAction(reportAction);

        } catch (error) {
            this.notification.add(
                error.message || "No se pudo generar el reporte excel.",
                {
                    title: "Error",
                    type: "danger",
                }
            );
            console.error("Error generando reporte:", error);
        } finally {
            this.state.loading = false;
        }
    }

    async downloadAccumulated() {
        try {
            this.state.loading = true;
            // Crear wizard
            const wizardId = await this.orm.create(
                "tyt.customized.report.wizard",
                [{
                    years: this.state.filters.selectedYears.toString() || "",
                    months: this.state.filters.selectedMonths.toString() || "",
                    department_ids: [[6,0, this.state.filters.departmentIds || []]],
                    pdomain_ids: [[6,0, this.state.filters.domainIds || []]],
                    process_ids: [[6,0, this.state.filters.processIds || []]],

                }]
            );

            const reportAction = await this.orm.call(
                "tyt.customized.report.wizard",
                "action_generate_accumulated_xlsx",
                [[wizardId]]
            );

            await this.action.doAction(reportAction);

        } catch (error) {
            this.notification.add(
                error.message || "No se pudo generar el reporte accumulado en excel.",
                {
                    title: "Error",
                    type: "danger",
                }
            );
            console.error("Error generando reporte:", error);
        } finally {
            this.state.loading = false;
        }
    }
}

registry.category("actions").add("tyt_risk_management.report_customized", CustomizedReport);
