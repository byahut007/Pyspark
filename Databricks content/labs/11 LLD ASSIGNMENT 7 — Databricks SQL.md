LLD ASSIGNMENT 7 — Databricks SQL


Case Scenario: “Retail BI Dashboard: Revenue & Top Products”


Business wants a dashboard that auto-updates hourly.

Functional Requirements
Create SQL Warehouse
Build queries:
Daily revenue
Top 20 products
Customer order counts
Create visualizations
Pin to dashboard
Configure scheduled refresh
Add alert for negative prices
LLD
Tables:
sales_daily_revenue_mv (materialized view)
Dashboard:
Line chart (daily revenue)
Bar chart (top products)
KPI widget (orders count)
Alert:
Alert:
SELECT COUNT(*) FROM sales WHERE price <= 0;

Non-functional Requirements
Dashboard refresh < 1 min
Warehouse auto-stop enabled

Acceptance Criteria
Dashboard accessible to business team
Alerts work