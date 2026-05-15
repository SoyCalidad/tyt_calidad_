/** @odoo-module **/

import {
    Component,
    onMounted,
    useRef,
    useState,
} from "@odoo/owl";

import { StatInfoCard } from "./stat_info_card";
import { PieChart } from "../pie_chart/pie_chart";

export class RiskSectionCard extends Component {

    static template = "tyt_risk_management.RiskSectionCard";

    static components = {
        StatInfoCard,
        PieChart,
    };

    static props = {
        title: String,
        data_status_risk: Array,
    };

    setup() {

        this.barChartRef = useRef("barChart");
        this.pieChartRef = useRef("pieChart");

        this.state = useState({
            collapsed: false,
        });

        onMounted(() => {
            this.renderBarChart();
        });
    }

    toggleCollapse() {
        this.state.collapsed = !this.state.collapsed;
    }

    renderBarChart() {

        const ctx = this.barChartRef.el.getContext("2d");

        this.barChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: [
                    "No mitigado",
                    "Parcialmente Mitigado",
                    "Mitigado",
                ],
                datasets: [{
                    data: this.props.data_status_risk || [0,0,0],

                    backgroundColor: [
                        "#ef4444",
                        "#f59e0b",
                        "#22c55e",
                    ],

                    borderRadius: 8,
                    maxBarThickness: 80,
                }],
            },

            options: {
                responsive: true,
                plugins: {
                    legend: {

                        position: "bottom",

                        labels: {

                            usePointStyle: true,
                            pointStyle: "circle",

                            generateLabels: (chart) => {

                                const dataset = chart.data.datasets[0];

                                return chart.data.labels.map((label, index) => ({
                                    text: `${dataset.data[index]} ${label}`,
                                    fillStyle: dataset.backgroundColor[index],
                                    strokeStyle: dataset.backgroundColor[index],
                                    hidden: false,
                                    index,
                                }));
                            },
                        },
                    },
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                        },
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 5,
                        },
                    },
                },
            },
        });
    }


}