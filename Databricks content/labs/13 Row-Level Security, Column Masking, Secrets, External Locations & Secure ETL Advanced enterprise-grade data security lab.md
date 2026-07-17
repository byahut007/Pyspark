LAB 16 — Row-Level Security, Column Masking, Secrets, External Locations & Secure ETL
Advanced enterprise-grade data security lab
Estimated Time: 3 hours


PART 0 — Setup


You will need:

✔ secured_catalog & retail_secure schema (from Lab 15)

✔ SQL Warehouse running


PART 1 — Column-Level Security (Masking Policies)


Step 1 — Create Masking Policy


As admin:

CREATE OR REPLACE MASKING POLICY email_masking AS
  (email STRING) RETURNS STRING ->
    CASE
      WHEN current_user() IN ("admin@company.com") THEN email
      ELSE CONCAT('***-MASKED-', RIGHT(email, 4))
    END;


Step 2 — Apply Masking Policy


Add a fake email column:

ALTER TABLE secured_catalog.retail_secure.retail_clean
ADD COLUMN customer_email STRING;
Update data:

UPDATE secured_catalog.retail_secure.retail_clean
SET customer_email = CONCAT(stock_code, "@example.com");
Apply masking:

ALTER TABLE secured_catalog.retail_secure.retail_clean
ALTER COLUMN customer_email
SET MASKING POLICY email_masking;


Step 3 — Test Masking
As admin:

SELECT stock_code, customer_email
FROM secured_catalog.retail_secure.retail_clean
LIMIT 5;
→ See full email.

Test user:

→ Should see masked email.



PART 2 — Row-Level Security (RLS)


Step 4 — Create RLS Policy
CREATE OR REPLACE ROW FILTER country_filter
FOR TABLE secured_catalog.retail_secure.retail_clean
AS (Country = current_user());
(This example assumes usernames match country codes; adjust as needed.)

Step 5 — Apply RLS
ALTER TABLE secured_catalog.retail_secure.retail_clean
SET ROW FILTER country_filter;
Test user can only see rows belonging to their allowed domain.



PART 3 — Secure External Locations (Cloud Storage)


Step 6 — Create Storage Credential
CREATE STORAGE CREDENTIAL retail_sc
WITH AZURE_MANAGED_IDENTITY;
Step 7 — Create External Location
CREATE EXTERNAL LOCATION retail_external
URL 'abfss://container@storageaccount.dfs.core.windows.net/external'
WITH STORAGE CREDENTIAL retail_sc;
Step 8 — Grant Access
GRANT READ FILES ON EXTERNAL LOCATION retail_external TO `test.user@demo.com`;
Test user can now query files without seeing storage keys.



PART 4 — Secrets Management


Step 9 — Create Secret Scope
Left nav → Compute → Advanced → Secret Scopes

Click Create Secret Scope

Name: lab16_scope

Step 10 — Add Secret
Add:

Key: db_password
Value: MySuperSecurePassword123!
Step 11 — Read Secret in Notebook
In Python notebook:

password = dbutils.secrets.get(scope="lab16_scope", key="db_password")
print(password[:5] + "***")
Secrets are never exposed in logs.



PART 5 — Secure ETL Design


Step 12 — Use Credential Passthrough
Under cluster → Edit
Enable:
Credential Passthrough
Restart cluster
Only permitted users access secure storage.

Step 13 — Secure ETL Notebook Pattern
Ingest with secure location:

df = spark.read.format("delta").load("abfss://secure/.../silver")

df.write.format("delta")\
    .option("overwriteSchema", "true")\
    .save("abfss://secure/.../gold")
Automatic identity-based access control applies.



PART 6 — Monitoring & Audit Logs


Step 14 — Open Audit Logs
Left nav → Admin Console → Audit Logs

Check:

Permission changes
Table access
Authentication events
Job runs
SQL queries

LAB 16 COMPLETE!


Learners now understand:

✔ Row-level security

✔ Column-level masking

✔ Masking Policies

✔ External locations

✔ Storage credentials

✔ Secrets

✔ Secure ETL patterns

✔ Credential passthrough

✔ Logs & auditing