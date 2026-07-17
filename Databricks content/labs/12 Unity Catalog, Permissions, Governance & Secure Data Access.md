LAB 15 — Unity Catalog, Permissions, Governance & Secure Data Access
Beginner → Intermediate full governance workflow

PART 0 — Prerequisites & Setup


Step 1 — Log in to Databricks
Browser → https://portal.azure.com
Sign in → open your Databricks workspace using Launch Workspace.
Wait for UI to load.
Step 2 — Confirm Unity Catalog is Enabled
In left navigation → click Catalog.
If you see:
Catalogs
Schemas
Tables
Lineage
Permissions tab
Then Unity Catalog is enabled.
If not, admin must enable UC.

(For the purpose of this lab, we assume UC is operational.)



Step 3 — Create a SQL Warehouse
(If you already have a running warehouse, skip)

Go to left menu → SQL.
Click SQL Warehouses.
Click Create Warehouse.
Name: lab15_security_wh
Cluster Size: Small
Auto-stop: 10 minutes
Enable serverless (if available)
Click Create → Start
Wait for green “Running”.

Step 4 — Create a Test User
(If you are the only user, simulate using a second user/role)

Admin Console (top-right gear icon)
Users → Add User
Add:
test.user@demo.com (dummy email)
Assign them “No special roles”.
We will use this identity for permission testing.



PART 1 — Creating a Governance Structure


We will create:

catalog: secured_catalog

schema: retail_secure

tables: retail_clean, retail_gold

Step 5 — Create a Catalog
Left menu → Catalog.
Click Create Catalog (top-right).
Enter:
Name: secured_catalog
Comment: “Secure Data Catalog for Lab 15”
Click Create.
Step 6 — Assign Ownership (Critical Step)
Click catalog: secured_catalog.
Click Permissions tab.
Click Grant → Add Principal.
Add:
Yourself as OWNER
test.user@demo.com — NO permissions yet
Save permissions.
Step 7 — Create Schema
Inside secured_catalog → click Create Schema.
Name: retail_secure.
Comment: “Retail tables with controlled access.”
Click Create.
Step 8 — Assign Schema Permissions
Open schema → click Permissions.
Grant USAGE to:
Yourself
Grant USAGE only to:
test.user@demo.com
Do NOT grant SELECT or MODIFY permissions yet.



PART 2 — Create Tables & Populate Data


Step 9 — Open SQL Editor
Left navigation → click SQL.
Click New → Query.
Select warehouse: lab15_security_wh.
Step 10 — Load Silver Data from Earlier Labs
Run:

CREATE OR REPLACE TABLE secured_catalog.retail_secure.retail_clean
AS SELECT * FROM lab13_retail;
Create gold table:

CREATE OR REPLACE TABLE secured_catalog.retail_secure.retail_gold AS
SELECT DATE(InvoiceDate) AS date,
       SUM(Quantity * UnitPrice) AS daily_revenue
FROM lab13_retail
GROUP BY DATE(InvoiceDate);

Step 11 — Explore Data
SELECT * FROM secured_catalog.retail_secure.retail_clean LIMIT 20;




PART 3 — Permission Testing (Deny by Default)

Step 12 — Switch to Test User
Open incognito window.

Log into Databricks with the test user account.

Navigate to:

Left menu → SQL → Data → secured_catalog → retail_secure

Expected behavior:

❌ Tables visible but you cannot query them

or

❌ Tables not visible at all (depending on UC config)


Step 13 — Try Running Query as Test User
Open SQL query editor and run:

SELECT * FROM secured_catalog.retail_secure.retail_clean;
Expected error:

❌ PERMISSION_DENIED: Missing SELECT privilege

This confirms security is correct.



PART 4 — Granting Select, Modify, Create Permissions


Step 14 — Grant SELECT
Back in your admin window:

GRANT SELECT ON TABLE secured_catalog.retail_secure.retail_clean
TO `test.user@demo.com`;
Test user runs:

SELECT * FROM secured_catalog.retail_secure.retail_clean LIMIT 5;
Now allowed.



Step 15 — Grant MODIFY
Enable insert/update/delete:

GRANT MODIFY ON TABLE secured_catalog.retail_secure.retail_clean
TO `test.user@demo.com`;


Have test user run:

INSERT INTO secured_catalog.retail_secure.retail_clean
VALUES ('12345','TEST',10,2.0,'2023-01-01','UK');
Expected: Works.



Step 16 — Revoke Permissions
Test governance reversibility:

REVOKE MODIFY ON TABLE secured_catalog.retail_secure.retail_clean
FROM `test.user@demo.com`;
Attempt insert as test user:

❌ Should fail.



PART 5 — Secure Functions, Views & Ownership


Step 17 — Create a Secure View
As admin:

CREATE OR REPLACE VIEW secured_catalog.retail_secure.v_revenue_secure
AS SELECT stock_code, Quantity * UnitPrice AS revenue
FROM secured_catalog.retail_secure.retail_clean;
Grant access:

GRANT SELECT ON VIEW secured_catalog.retail_secure.v_revenue_secure
TO `test.user@demo.com`;
Test user can now run:

SELECT * FROM secured_catalog.retail_secure.v_revenue_secure LIMIT 10;
Step 18 — Transfer Ownership (Rare but useful)
ALTER TABLE secured_catalog.retail_secure.retail_clean
OWNER TO `test.user@demo.com`;
Test user tests they can now:

Grant permissions
Revoke permissions
Drop table
Then revert:

ALTER TABLE secured_catalog.retail_secure.retail_clean
OWNER TO current_user();


PART 6 — Auditing, Lineage & Access Logs


Step 19 — Lineage Observation
Open left nav → Catalog
Navigate to table → click Lineage
Observe:
Upstream: views
Downstream: dashboards
Job producers
Step 20 — View Query History (Audit Trail)
Left menu → SQL → Query History

Filter by:

User
Warehouse
Status
You can see actions by the test user — acts as audit logs.



LAB 15 COMPLETE!


Learners now understand:

✔ Catalog/schema/table permissions

✔ Granting + revoking privileges

✔ Secure views

✔ Ownership transfer

✔ Lineage

✔ Query auditing