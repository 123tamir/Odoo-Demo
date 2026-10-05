/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";
import {
    Component, onMounted, onWillStart, onWillUnmount, useRef, useState,
} from "@odoo/owl";

const fmtDate = (d) => d.toISOString().slice(0, 10);

export class SalesDashboard extends Component {
    static template = "sales_dashboard.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.trendRef = useRef("trendChart");
        this.productRef = useRef("productChart");
        this.charts = {};

        const today = new Date();
        const start = new Date();
        start.setDate(today.getDate() - 180);

        this.state = useState({
            dateFrom: fmtDate(start),
            dateTo: fmtDate(today),
            data: {
                total_sales: 0, order_count: 0, avg_order: 0,
                low_stock_count: 0, low_stock: [], top_products: [], monthly: [],
            },
        });

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            await this.loadData();
        });
        onMounted(() => this.renderCharts());
        onWillUnmount(() => Object.values(this.charts).forEach((c) => c.destroy()));
    }

    async loadData() {
        this.state.data = await this.orm.call(
            "sd.sale", "get_dashboard_data",
            [this.state.dateFrom, this.state.dateTo]
        );
    }

    async onDateChange(field, ev) {
        this.state[field] = ev.target.value;
        await this.loadData();
        this.renderCharts();
    }

    fmtMoney(value) {
        return "₹" + new Intl.NumberFormat("en-IN", { maximumFractionDigits: 0 }).format(value || 0);
    }

    drawChart(key, canvas, type, labels, values, label) {
        if (this.charts[key]) {
            this.charts[key].destroy();
        }
        this.charts[key] = new window.Chart(canvas, {
            type,
            data: {
                labels,
                datasets: [{
                    label,
                    data: values,
                    backgroundColor: "rgba(113, 75, 103, 0.6)",
                    borderColor: "#714b67",
                    borderWidth: 2,
                }],
            },
            options: { responsive: true, maintainAspectRatio: false },
        });
    }

    renderCharts() {
        const d = this.state.data;
        this.drawChart("trend", this.trendRef.el, "line",
            d.monthly.map((m) => m.label), d.monthly.map((m) => m.amount), "Sales per month");
        this.drawChart("products", this.productRef.el, "bar",
            d.top_products.map((p) => p.name), d.top_products.map((p) => p.amount), "Top 5 products");
    }
}

registry.category("actions").add("sales_dashboard.dashboard", SalesDashboard);