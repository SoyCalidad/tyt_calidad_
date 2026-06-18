/** @odoo-module */

import { Component, useState, onWillStart, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";

import { MONTHS } from "../../utils";


class RPEAppetiteLevelReport extends Component {
    static template = 'tyt_risk_management.RPEAppetiteLevel';

    static components = {
        Layout,
    };

    setup() {

        this.notification = useService("notification");
        this.orm = useService("orm");
        this.state = useState({
            filters: {

                department_id: "0",
                year: "0",
                cr_period: "tri",
                revision_type: "0",
            },

            //data filters 
            loading: false,
            years: [],
            departments: [],
        });

        this.reportData = useState({
            "report": [],
            "totales": {
                "periodos": [],
            }
        });

        this.dialog = useService("dialog");
        onWillStart(async () => {
            await this.loadFilters();

            this.onSearch()
        });



    }

    getColorApetite(apetite) {
    if (apetite == 'Alto') {
        return '#c22f1b'
    }
    else if(apetite == 'Moderado') {
        return '#FFD700'
    } else {
        return '#9ACD32'
    }
}


    async loadFilters() {
        await this.loadDepartments();
        try {
            const availableYears = await this.orm.call(
                "tyt.risk.mitigation",
                "get_available_years",
                []
            );
            this.state.years = availableYears;
            if (availableYears) {
                this.state.filters.year = availableYears[0];
            }
        } catch (error) {
            this.notification.add(
                "Errror al cargar los años",
                {type: "danger"},
            )
            console.error("Error cargando anos:", error);
        }


    }
    async loadDepartments() {
        try {
            const data = await this.orm.searchRead(
                "hr.department",
                [['x_studio_npp', '=', 1]],
                ["id", "name",]
            );
            this.state.departments = data ;
        } catch (error) {
            console.error("Error cargando domains:", error);
        }
    }


    async openMitigation(mIds = []) {
        console.log("mids", mIds);
        await this.dialog.add(MitigationModal, {
            title: "Lista de riesgos",
            mIds,
            actionId: this.idActionActivity,
            showAction: true,
        });
    }

    async onSearch() {
        try {
            this.state.loading = true;
            const data = await this.orm.call(
                "tyt.risk.mitigation",     
                "rpe_appetite_level_report", 
                [ 
                    this.state.filters.department_id, 
                    this.state.filters.year,
                    this.state.filters.cr_period,
                    this.state.filters.revision_type,
                ]
            );
            this.reportData.report = data.report;
            this.reportData.totales = data.totales;
            console.log("reportdata", this.reportData)

        } catch (error) {
            console.error("Error carga de report:", error);
            this.notification.add(
                "Errror al cargar el reporte",
                {type: "danger"},
            )
        } finally {
            this.state.loading = false;
        }
    }
}

registry.category("actions").add("tyt_risk_management.rpe_appetite_level_report", RPEAppetiteLevelReport);
