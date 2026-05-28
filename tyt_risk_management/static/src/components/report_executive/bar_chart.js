
import { Component, onMounted, onWillUnmount, onWillUpdateProps, useRef } from "@odoo/owl";
import { loadBundle } from "@web/core/assets";

export class BarChart extends Component {
    static template = "tyt_risk_management.REBarChart";

    static props = {
        series: {
            type: Array,
            // [{ name: "Riesgos Asegurados", data: [1, 0, 0], color: "#28a745" }]
        },
        categories: {
            type: Array,
            // ["Operativo,Estrategico", "Cumplimiento", "Operativo"]
        },
        title:      { type: String,  optional: true },
        height:     { type: Number,  optional: true },
        showLegend: { type: Boolean, optional: true },
        horizontal: { type: Boolean, optional: true },
        stacked:    { type: Boolean, optional: true },
    };

    static defaultProps = {
        title:      "",
        height:     350,
        showLegend: true,
        horizontal: false,
        stacked:    false,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chartInstance = null;

        onMounted(async () => {
            // Carga Chart.js desde el bundle nativo de Odoo 18
            await loadBundle("web.chartjs_lib");
            this._initChart();
        });

        onWillUpdateProps((nextProps) => {
            this._updateChart(nextProps);
        });

        onWillUnmount(() => {
            this._destroyChart();
        });
    }

    _buildConfig(props) {
        const { series, categories, showLegend, horizontal, stacked } = props;

        return {
            type: horizontal ? "bar" : "bar",
            data: {
                labels: categories,
                datasets: series.map((s) => ({
                    label:           s.name,
                    data:            s.data,
                    backgroundColor: s.color || "#378ADD",
                    borderColor:     s.color || "#378ADD",
                    borderWidth:     0,
                    borderRadius:    4,
                    borderSkipped:   false,
                })),
            },
            options: {
                indexAxis:   horizontal ? "y" : "x",
                responsive:  true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display:  showLegend,
                        position: "bottom",
                        labels: {
                            usePointStyle: true,
                            pointStyle:    "circle",
                            padding:       20,
                            font:          { size: 12 },
                        },
                    },
                    tooltip: {
                        callbacks: {
                            label: (ctx) =>
                                ` ${ctx.dataset.label}: ${ctx.parsed[horizontal ? "x" : "y"]}`,
                        },
                    },
                },
                scales: {
                    x: {
                        stacked: stacked,
                        grid:    { display: !horizontal },
                        ticks:   { font: { size: 11 } },
                    },
                    y: {
                        stacked:    stacked,
                        beginAtZero: true,
                        grid:        { display: horizontal },
                        ticks:       { font: { size: 11 } },
                    },
                },
            },
        };
    }

    _initChart() {
        const canvas = this.canvasRef.el;
        if (!canvas || !window.Chart) return;

        this.chartInstance = new window.Chart(
            canvas,
            this._buildConfig(this.props)
        );
    }

    _updateChart(props) {
        if (!this.chartInstance) return;

        const config = this._buildConfig(props);

        // Actualiza datasets y labels sin destruir el canvas
        this.chartInstance.data.labels   = config.data.labels;
        this.chartInstance.data.datasets = config.data.datasets;
        this.chartInstance.options       = config.options;
        this.chartInstance.update();
    }

    _destroyChart() {
        if (this.chartInstance) {
            this.chartInstance.destroy();
            this.chartInstance = null;
        }
    }
}