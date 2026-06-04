/** @odoo-module */

import { Component, useState, onWillStart, useRef  } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { loadBundle } from "@web/core/assets";
import { loadJS } from "@web/core/assets";

import { PieChart } from "../pie_chart/pie_chart";
import { CollapsibleCard } from "../collapsible_card/collapsible_card";
import { MONTHS } from "./../utils";
import { BarChart } from "./bar_chart";
import { RiskMap } from "./../report_consolidated/risk_map/risk_map";

export class ExecutiveReport extends Component {
    static template = 'tyt_risk_management.executive_report';

    static components = { 
        Layout, 
        PieChart, 
        CollapsibleCard,
        BarChart ,
        RiskMap,
    };

    setup() {

        this.orm = useService("orm");
        this.state = useState({
            filters: {
                department_id: "0",
                domain_id: "0",
                process_id: "0",
                year: '0',
                month: '0',
            },

            //data filters 
            loading: false,
            processes: [],
            domains: [],
            months: MONTHS,
            years: [],
            departments: [],
        });

        this.reportData = useState({
        });

        this.dialog = useService("dialog");
        this.uninsuredRisksChart = useRef("uninsured-risks-chart");
        this.barchartGradoRef = useRef("chart-grado-empresa");
        this.gaugeDegreeComplianceRef = useRef("chart-degree-compliance");
        this.chartImpactCompanyRef = useRef("chart-impact-company");
        this.maturityLevelChart = useRef("maturity-level-chart");
        onWillStart(async () => {
            await loadJS("/tyt_risk_management/static/lib/echarts/echarts.min.js");
            await loadBundle("web.chartjs_lib")
            await this.loadFilters();
            
            //defaul year and month 
            const today = new Date();
            const anio = today.getFullYear() 
            const month = today.getMonth()
            if (this.state.years.includes(anio)) {
                this.state.filters.anio = anio;
            }
            if (month) {
                this.state.filters.month = month.toString();
            }
            await this.onSearch()
        });
    }

    loadUninsuredRisksChart() {
        const chartDom = this.uninsuredRisksChart.el;
        if (chartDom) {
            var myChart = echarts.init(chartDom);
            const option = {
                tooltip: {
                    trigger: 'item'
                },
                series: [
                    {
                    name: '',
                    type: 'pie',
                    radius: '50%',
                    data: this.reportData?.report?.objetivos.map(item => ({value: item.no_asegurados, 'name': item.objetivo})) || [],
                    emphasis: {
                        itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 1)'
                        }
                    }
                    }
                ]
                };
    
            option && myChart.setOption(option);

        }

    }
    loadMadurityLevelChart() {
        const chartDom = this.maturityLevelChart.el;
        if (chartDom) {
            var myChart = echarts.init(chartDom);
            const nivel_madurez = this.reportData?.report?.nivel_madurez || []
            const option = {
                tooltip: {
                    trigger: 'item'
                },
                series: [
                    {
                    name: '',
                    type: 'pie',
                    radius: '50%',
                    data: nivel_madurez.map(item => ({
                        value: item.cantidad,
                        name: item.nivel,
                    })) || [],
                    //data:  [],
                    emphasis: {
                        itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 1)'
                        }
                    }
                    }
                ]
                };
    
            option && myChart.setOption(option);

        }

    }
    loadGauge() {

        const chartDom = this.gaugeDegreeComplianceRef.el;
        if (chartDom) {
            var myChart = echarts.init(chartDom);
            var option;
    
            option = {
                series: [
                    {
                    type: 'gauge',
                    startAngle: 180,
                    endAngle: 0,
                    center: ['50%', '75%'],
                    radius: '90%',
                    min: 0,
                    max: 1,
                    splitNumber: 20,
                    axisLine: {
                        lineStyle: {
                            width: 6,
                            color: [
                                [0.5, '#FF6E76'],
                                [0.75, '#FDDD60'],
                                [1, '#7CFFB2']
                            ]
                        }
                    },
                    pointer: {
                        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                        length: '60%',
                        width: 12,
                        offsetCenter: [0, '0%'],
                        itemStyle: {
                        color: 'auto'
                        }
                    },
                    axisTick: {
                        length: 15,
                        lineStyle: {
                        color: 'auto',
                        width: 1
                        }
                    },
                    splitLine: {
                        length: 20,
                        lineStyle: {
                          color: 'auto',
                          width: 2
                        }
                    },
                    axisLabel: {
                        color: '#464646',
                        fontSize: 10,
                        distance: -40,
                        rotate: 'tangential',
                        formatter: function (value) {
                        if (value == 0.85) {
                            return 'Satisfactorio';
                        } else if (value == 0.65) {
                            return 'Necesita mejora';
                        } else if (value == 0.25) {
                            return 'No satisfactorio';
                        }
                        return '';
                        }
                    },
                    title: {
                        offsetCenter: [0, '-10%'],
                        fontSize: 18
                    },
                    detail: {
                        fontSize: 30,
                        offsetCenter: [0, '-40%'],
                        valueAnimation: true,
                        formatter: function (value) {
                        return Math.round(value * 100) + ' %';
                        },
                        color: 'inherit'
                    },
                    data: [
                        {
                        value: this.reportData?.report?.per_mitigation_safe || 0,
                        name: ''
                        }
                    ]
                    }
                ]
            };
    
            option && myChart.setOption(option);

        }

    }

    loadLevelComplain() {
        const chartDom = this.barchartGradoRef.el;
        if (chartDom) {
            var myChart = echarts.init(chartDom);
            var option;
    
            option = {
                yAxis: {
                    type: 'category',
                    data: this.reportData?.report?.degree_of_compliance_company.map(degree => degree.department_name || "") || [],
                },
                xAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: this.reportData?.report?.degree_of_compliance_company.map(degree => degree.grado_cumplimiento || 0) || [],
                        type: 'bar'
                    }
                ]
            };
    
            option && myChart.setOption(option);

        }
    }

    loadImpactCompanyChart() {
        const chartDom = this.chartImpactCompanyRef.el;
        if (chartDom) {
            var myChart = echarts.init(chartDom);
            var option;
    
            option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                    type: 'shadow'
                    }
                },
                yAxis: {
                    type: 'category',
                    data: this.reportData?.report?.degree_of_compliance_company.map(degree => degree.department_name || "") || [],
                },
                xAxis: {
                    type: 'value',
                    boundaryGap: [0, 0.01],
                },
                series: [
                    {
                        data: this.reportData?.report?.degree_of_compliance_company.map(degree => degree.grado_cumplimiento_residual || 0) || [],
                        type: 'bar'
                    }
                ]
            };
    
            option && myChart.setOption(option);

        }
    }

    get cosoCategories() {
        return (this.reportData?.report?.objetivos || [])
            .map((o) => o.objetivo);
    }
    get cosoChartSeries() {
        const objetivos = this.reportData?.report?.objetivos || [];
        return [
            {
                name:  "Riesgos Asegurados",
                color: "#28a745",
                data:  objetivos.map((o) => o.asegurados),
            },
            {
                name:  "Riesgos No Asegurados",
                color: "#dc3545",
                data:  objetivos.map((o) => o.no_asegurados),
            },
        ];
    }

    onChangeDomain() {
        console.log("onchangedomain", this.state.filters.domain_id);
        this.cargarProcesos()
    }

    async loadFilters() {
        await this.loadDomains();
        await this.cargarProcesos();
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
            const data = await this.orm.searchRead(
                "hr.department",
                [['x_studio_npp', '=', 1]],
                ["id", "name",]
            );
            this.state.departments = data;
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

            this.state.domains = data;
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
            this.state.processes = data;
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
            showAction: true,
        });
    }

    async onSearch() {
        this.state.loading = true;
        try {
            const data = await this.orm.call(
                "tyt.risk.mitigation",     
                "report_executive", 
                [
                    this.state.filters.department_id,
                    this.state.filters.domain_id,
                    this.state.filters.process_id,
                    this.state.filters.year,
                    this.state.filters.month,
                ]
            );
            this.reportData = data;

        } catch (error) {
            console.error("Error cargando search:", error);
        }
        this.state.loading = false;
        setTimeout(() => {
            this.loadGauge();
            this.loadLevelComplain();
            this.loadImpactCompanyChart();
            this.loadMadurityLevelChart();
            this.loadUninsuredRisksChart();
        }, 500);
    }
}

registry.category("actions").add("tyt_risk_management.report_executive", ExecutiveReport);
