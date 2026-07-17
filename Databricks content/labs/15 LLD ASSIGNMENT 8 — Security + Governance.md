LLD ASSIGNMENT 8 — Security + Governance


Case Scenario: “Secure Access for External Analyst Team”
A partner analytics team needs access only to aggregated Gold data, not raw data.


Functional Requirements
Create catalog: partner_secure
Create schema: analytics
Move Gold tables
Grant:
USAGE on catalog
SELECT on Gold tables
Mask PII
Row-level access by region

LLD
Masking:
CREATE MASKING POLICY email_mask AS (email STRING) RETURNS STRING -> '***MASKED***';
RLS:
CREATE ROW FILTER region_filter FOR TABLE sales_gold AS (region = current_user());

Non-functional Requirements
Zero access to Bronze/Silver
Full lineage traceability

Acceptance Criteria
Partner user ONLY sees Gold
PII masked
Region-based filtering enforced