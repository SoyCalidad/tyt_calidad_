/** @odoo-module **/

import {
    Component,
    onMounted,
    onWillStart,
    onWillUnmount,
    useRef,
} from "@odoo/owl";

import { loadBundle } from "@web/core/assets";

export class MaturityBarChart extends Component {

    static template = "tyt_risk_management.MaturityBarChart";

    static props = {
        title: String,
        data: Array,
        labels: Array,
        colors: Array,
    };

    setup() {

        this.chartRef = useRef("chart");

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib");
        });

        onMounted(() => {
            this.renderChart();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {

        const ctx = this.chartRef.el.getContext("2d");

        this.chart = new Chart(ctx, {

            type: "bar",

            data: {

                labels: this.props.labels,

                datasets: [{
                    data: this.props.data,

                    backgroundColor: this.props.colors,

                    borderRadius: 8,

                    maxBarThickness: 70,
                }],
            },

            options: {

                responsive: true,
                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false,
                    },

                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                return `${context.raw}`;
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
                            precision: 0,
                        },
                    },
                },
            },
        });
    }
}