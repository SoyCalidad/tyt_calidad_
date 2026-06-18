/** @odoo-module */

import { Component, useState, onWillStart, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";

import { MONTHS } from "../../utils";

const MAP = {
        'severe': "background-color: #8B0000; color: #fff; font-weight: bold; font-size: 14px;",
        'higher':" background-color: #DC3545; color: #fff; font-weight: bold; font-size: 14px;",
        'significant':  "background-color: #FFC107; color: #222; font-weight: bold; font-size: 14px;",
        'minor':  "background-color: #008000; color: #fff; font-weight: bold; font-size: 14px;",
        'insignificant':  "background-color: #28A745; color: #fff; font-weight: bold; font-size: 14px;",
    };

class RPERiskRatingReport extends Component {
    static template = 'tyt_risk_management.RPERiskRating';

    static components = {
        Layout,
    };

    nivelStyle(nivel) {
        
        return MAP[nivel] ?? '';
    }

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
            "totals": {
                "periodos": [],
            },
            "periods": [],
        });

        this.dialog = useService("dialog");
        onWillStart(async () => {
            await this.loadFilters();

            this.onSearch()
        });



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
                "rpe_risk_rating", 
                [ 
                    this.state.filters.department_id, 
                    this.state.filters.year,
                    this.state.filters.cr_period,
                    this.state.filters.revision_type,
                ]
            );
            this.reportData.report = data.report;
            this.reportData.totals = data.totals;
            this.reportData.periods = data.periods;
            console.log("reportdata", this.reportData);

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

registry.category("actions").add("tyt_risk_management.rpe_risk_rating_report", RPERiskRatingReport);
