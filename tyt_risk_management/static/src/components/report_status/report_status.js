/** @odoo-module */

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { loadBundle } from "@web/core/assets";

import { PieChart } from "../pie_chart/pie_chart";
import {CollapsibleCard } from "../collapsible_card/collapsible_card";
import { MitigationModal } from "./mitigation_modal/mitigation_modal";


export class Nivel2StatusReport extends Component {
    static template = 'tyt_risk_management.report_nivel2_status';
    static components = { Layout, PieChart, CollapsibleCard, MitigationModal   };

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            filters: {
                domain_id: false,
                process_id: false,
                year: 'all',
                month: 'all',
            },
            data: [],
            processedData: [
                {
                    "process_id": "46e7694e-a647-462d-9421-9955f529998c",
                    "process_short_name": "ASG",
                    "process_name": "Sostenibilidad",
                    "total": 41,
                    "registros_total": [2,3,4],
                    "is_not_scope": 0,
                    "registros_is_not_scope": [],
                    "is_open": 36,
                    "registros_is_open": [ 2  ],
                    "is_review": 2,
                    "registros_is_review": [2,3
                    ],
                    "is_remediation": 2,
                    "registros_is_remediation": [ 2
                    ],
                    "is_audit": 0,
                    "registros_is_audit": [],
                    "is_completed": 1,
                    "registros_is_completed": [ 2
                    ],
                    "is_completed_percentage": 2,
                    
                    "no_completed": 40,
                    "registros_no_completed": [
                        2,6,3,2
                    ],
                    "subProcesos": [
                        {
                            "sub_process_id": "93be569b-d103-4503-8189-1813d202adbb",
                            "sub_process_name": "Ambiental_Social_Gobernanza",
                            "total": 41,
                            "registros_total": [2,3],
                            "is_not_scope": 0,
                            "registros_is_not_scope": [],
                            "is_open": 36,
                            "registros_is_open": [2,3],
                            "is_review": 2,
                            "registros_is_review": [3],
                            "is_remediation": 2,
                            "registros_is_remediation": [2,3],
                            "is_audit": 0,
                            "registros_is_audit": [],
                            "is_completed": 1,
                            "registros_is_completed": [2
                            ],
                            "is_completed_percentage": {
                                "source": "2.00",
                                "parsedValue": 2
                            },
                            "no_completed": 40,
                            "registros_no_completed":  [2,3,4]
                        }
                    ]
                }

            ],

            //data filters 
            processes: [],
            domains: [],
            months: [
                { id: 1, name: 'Enero' },
                { id: 2, name: 'Febrero' },
                { id: 3, name: 'Marzo' },
                { id: 4, name: 'Abril' },
                { id: 5, name: 'Mayo' },
                { id: 6, name: 'Junio' },
                { id: 7, name: 'Julio' },
                { id: 8, name: 'Agosto' },
                { id: 9, name: 'Setiembre' },
                { id: 10, name: 'Octubre' },
                { id: 11, name: 'Noviembre' },
                { id: 12, name: 'Diciembre' },
            ],
            years: [],
            departments: [],
        });

        this.dialog = useService("dialog");

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib")
            await this.loadFilters();
            await this.fetchInitialData();

            this.processDataForCards();

        });
    }

    async loadFilters() {
        await this.cargarProcesos();
        await this.loadDomains();
        await this.loadDepartments();
        const availableYears = await this.orm.call(
            "tyt.risk.mitigation",     
            "get_available_years", 
            []
        );

        this.state.years = availableYears;

        
    }
    async loadDepartments() {
        try {
            const data = await this.orm.searchRead("hr.department", [], ["id", "name",]);
            this.state.departments = data;
        } catch (error) {
            console.error("Error cargando domains:", error);
        }
    }

    async loadDomains() {
        try {
            const data =  await this.orm.searchRead(
                "tyt.business.process", 
                [["nivel", "=", 1]],
                ["id", "name", "short_name"],
            );
            
            this.state.domains = data;
        } catch (error) {
            console.error("Error cargando domains:", error);
        }
    }

    async cargarProcesos() {
        try {
            const data = await this.orm.searchRead(
                "tyt.business.process", 
                [["nivel", "=", 2]],
                ["id", "name", "short_name"]);
            this.state.processes = data;
        } catch (error) {
            console.error("Error cargando procesos:", error);
        }
    }

    async fetchInitialData() {
        // Simulación de carga de datos basada en tu JSON
        // En producción: this.state.data = await this.orm.call(...)
        this.state.data = [/* Tu JSON aquí */];

        const actionId = await this.orm.call(
            "tyt.risk.mitigation",
            "get_form_action_id",
            [[]]
        );
        this.idActionActivity = actionId; //actionId
    }

    processDataForCards() {
        const result = {
            completed: [],
            keyControls: [],
            unmitigated: []
        };

        this.state.data.forEach(proc => {
            const records = proc.registros_total || [];

            // FILTRADO LÓGICO (Si no es 'all', filtrar)
            const filteredRecords = records.filter(r => {
                const matchYear = this.state.filters.year === 'all' || r.year === this.state.filters.year;
                const matchMonth = this.state.filters.month === 'all' || r.month_name === this.state.filters.month;
                return matchYear && matchMonth;
            });

            if (filteredRecords.length === 0 && this.state.filters.year !== 'all') return;

            // 1. Cálculo de Completados (Porcentaje)
            // Asumimos completado si status no es 'sys_unmitigated'
            const completedCount = filteredRecords.filter(r => r.status !== 'sys_unmitigated').length;
            const percentage = filteredRecords.length > 0
                ? Math.round((completedCount / filteredRecords.length) * 100)
                : 0;

            result.completed.push({
                name: proc.process_short_name,
                value: `${percentage}%`
            });

            // 2. Controles Claves (isaudit == true)
            const keyCount = filteredRecords.filter(r => r.isaudit === true).length;
            result.keyControls.push({
                name: proc.process_short_name,
                value: keyCount
            });

            // 3. No Mitigados (status == 'sys_unmitigated')
            const unmitigatedCount = filteredRecords.filter(r => r.status === 'sys_unmitigated').length;
            result.unmitigated.push({
                name: proc.process_short_name,
                value: unmitigatedCount
            });
        });

        //this.state.processedData = result;
    }

    async openMitigation(mIds = []) {
        console.log("mids", mIds);
        await this.dialog.add(MitigationModal, {
            title: "Lista de riesgos",
            mIds,
            actionId: this.idActionActivity,
        });
    }

    onSearch() {
        this.processDataForCards();
    }
}

registry.category("actions").add("tyt_risk_management.nivel2statusreport", Nivel2StatusReport);
