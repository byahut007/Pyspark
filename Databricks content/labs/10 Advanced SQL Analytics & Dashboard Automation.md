LAB 14 — Advanced SQL Analytics & Dashboard Automation
Estimated Time: 2.5 hours

Goal: Learn joins, window functions, views, materialized views, dashboards, alerts, BI-ready datasets, and organizational workflows.


PART 0 — Setup


Step 1 — Ensure SQL Warehouse Running


SQL → Warehouses → Start the warehouse.



PART 1 — Create Analytical Views


Step 2 — Create a Revenue View
Run:

CREATE OR REPLACE VIEW retail_revenue AS
SELECT
    stock_code,
    SUM(Quantity * UnitPrice) AS revenue
FROM lab13_retail
GROUP BY stock_code;
Check:

SELECT * FROM retail_revenue LIMIT 10;


Step 3 — Create Materialized View
Run:

CREATE OR REPLACE MATERIALIZED VIEW mv_daily_revenue
AS
SELECT
  DATE(InvoiceDate) AS day,
  SUM(Quantity * UnitPrice) AS revenue
FROM lab13_retail
GROUP BY day;
This automatically refreshes.

Check refresh:

Data → your schema → mv_daily_revenue → Details
You’ll see:
Refresh history
Status

PART 2 — Complex Joins


Step 4 — Join Silver and Dim Tables
If you have dim_small from previous labs:

SELECT a.stock_code, b.stock_code AS dim_code
FROM lab13_retail a
LEFT JOIN dim_small b
ON a.stock_code = b.stock_code;


PART 3 — Window Functions


Step 5 — Ranking
SELECT
  stock_code,
  SUM(Quantity) AS qty,
  RANK() OVER(ORDER BY SUM(Quantity) DESC) AS rank
FROM lab13_retail
GROUP BY stock_code;
Step 6 — Running Totals
SELECT
  DATE(InvoiceDate) AS date,
  SUM(Quantity * UnitPrice) AS revenue,
  SUM(SUM(Quantity * UnitPrice)) OVER(ORDER BY DATE(InvoiceDate)) AS running_revenue
FROM lab13_retail
GROUP BY DATE(InvoiceDate);


PART 4 — Build BI Dashboard
Step 7 — Create 3 Visualizations


Visualization 1 — Total Revenue Trend
Run:

SELECT DATE(InvoiceDate) AS date, SUM(Quantity*UnitPrice) AS revenue
FROM lab13_retail
GROUP BY date
ORDER BY date;
Switch to Line Chart.


Visualization 2 — Top Products
Run:

SELECT stock_code, SUM(Quantity*UnitPrice) AS rev
FROM lab13_retail
GROUP BY stock_code
ORDER BY rev DESC
LIMIT 15;
Visualization → Bar Chart.


Visualization 3 — Running Revenue
Use earlier window function → Area Chart.

Step 8 — Create Dashboard
Open any visualization → click Pin.
Choose: Create new dashboard → lab14_analytics_dashboard.
Add all 3 visualizations.
Resize + arrange.

PART 5 — Alerts & Automation

Step 9 — Create Data Quality Alert
Run:

SELECT COUNT(*) AS null_desc
FROM lab13_retail
WHERE description IS NULL;
Create alert:

Name: DescriptionNullCheck
Condition: null_desc > 0
Schedule: Daily
Notification: Email


PART 6 — Automate Dashboard Refresh


Step 10 — Create Dashboard Task
SQL → Dashboards → open your dashboard.
Click Schedule.
Choose:
Refresh every day
Warehouse: same warehouse
Save.

LAB 14 COMPLETE!


Learners now master:

✔ Views + Materialized Views

✔ Complex joins

✔ Window functions

✔ BI dashboards

✔ Alerts + scheduling

✔ Dashboard automation

✔ SQL warehouse optimization