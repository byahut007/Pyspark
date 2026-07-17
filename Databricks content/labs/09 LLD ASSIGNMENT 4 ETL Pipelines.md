LLD ASSIGNMENT 4 — ETL Pipelines


Case Scenario: “Full Retail ETL Orchestration using Workflows”
RetailCorp needs an end-to-end ETL orchestration for daily transaction processing.

Functional Requirements
Create multi-task workflow:
Bronze ingestion
Silver cleaning
Gold aggregation
Quality validation task
Each task must run on a job cluster
Use widgets for parameters
Configure retries
LLD
Job structure:
Task1: ingest_raw   (Notebook)
Task2: silver_clean (Notebook, depends on Task1)
Task3: gold_agg     (Notebook, depends on Task2)
Task4: dq_check     (Notebook, depends on Task3)
Job cluster config: DBR 14.x, autoscale 1–3
DQ notebook:
Check for null critical fields
If nulls found → raise exception


Non-functional Requirements
Pipeline must run under 10 minutes
Retries: 3 attempts with 20s delay
Acceptance Criteria
Workflow DAG correct
Pipeline runs successfully end-to-end
DQ checks enforced
