# Odoo 17 Sales Dashboard

A custom Odoo 17 module with its own models, `read_group` aggregations,
and an OWL client-action dashboard (KPI tiles, Chart.js charts, date filter).

## Features
- Custom models: sd.sale, sd.product, sd.customer (computed and indexed fields)
- Sample data generated on install, with no Odoo demo data
- Dashboard: total sales, order count, average order value, low-stock alerts
- Pivot, graph, list and form views with filters and group-by

## Run it
```bash
docker compose up -d
```
1. Open http://localhost:8069 and create a database (leave Demo Data unticked).
2. Go to http://localhost:8069/web?debug=1, then Apps, then Update Apps List.
3. Search "Sales Dashboard" and click Activate.
4. Open Sales Dashboard, then Dashboard.

## Demo video
(add link here)