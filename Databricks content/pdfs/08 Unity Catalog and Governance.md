Unity Catalog Overview
• Unified governance layer for all Databricks
Lakehouse assets
• Controls access to data, files, ML models,
dashboards
• Centralizes metadata, permissions, and
lineage
• Supports multi-cloud and cross-workspace
governance
• Enterprise-grade security and compliance
foundation
Why Unity Catalog?
• Solves fragmented governance across
workspaces
• Provides consistent fine‑grained access
control
• Centralizes audit, lineage, and metadata
• Supports data sharing without data
duplication
• Essential for regulated industries
Unity Catalog Architecture
• Three-level namespace: Catalog →
Schema → Table
• Applies governance uniformly at all
levels
• Supports external locations and
storage credentials
• Metadata stored securely with
managed endpoints
• Works with SQL Warehouses and
Lakehouse compute
Catalogs, Schemas & Tables
• Catalog: Highest organizational boundary
• Schema: Logical grouping of data objects
• Tables: Delta Lake-based storage
• Supports views, functions, models, volumes
• Improves clarity and controlled access
Storage Credentials & External
Locations
• Allow secure access to cloud storage
• Use identity-based access configurations
• Supports AWS IAM, Azure Managed Identity, GCP SA
• Manage policy boundaries for external tables
• Enable unified governance across cloud data
Managed vs External Tables
• Managed tables stored in Unity
Catalog-managed locations
• External tables reference existing cloud
storage
• Both enforce UC governance and
logging
• Managed simplifies lifecycle operations
• External offers flexibility for
BYO‑storage
Data Lineage Capabilities
• Automatically captures data movement
• Column-level lineage for transformations
• Supports notebooks, jobs, SQL queries
• Visual lineage graph in the UI
• Improves debugging, auditing, and governance
Delta Sharing with Unity Catalog
• Share data securely across accounts/clouds
• Uses open Delta Sharing protocol
• No data replication required
• Recipient-based secure access
• Ideal for B2B data exchange
Unity Catalog for Machine Learning
• Governs MLflow models and artifacts
• Tracks lineage from datasets to
models
• Centralizes permissions for model
access
• Supports model versioning and
auditability
• Enhances MLOps governance
Unity Catalog Volumes
• Governed file storage replacing DBFS
• Supports unstructured and
semi‑structured files
• Used for ML training data, media,
feature data
• Permissions aligned with catalogs &
schemas
• Better auditing than legacy DBFS paths
Governance Overview with Unity
Catalog
• Enterprise-grade governance across data, AI, analytics
• Identity-based access control
• Audit-ready architecture
• Unified policies across workspaces
• Consistent governance for all assets
Unity Catalog Permission Model
• Supports GRANT/REVOKE at catalog/schema/table levels
• Hierarchical permission inheritance
• Fine‑grained privileges for all asset types
• Supports service principals and groups
• Simplifies enterprise RBAC
Table-Level Security
• Control SELECT, MODIFY, CREATE,
OWN privileges
• Restrict unauthorized read/write
access
• Enable secure BI and analytics
workflows
• Critical for confidential datasets
• Works uniformly across SQL & ML
workloads
Column-Level Security
• Mask or hide sensitive fields
• Apply data classification policies
• Dynamic data masking rules
• Protect PII/PHI across teams
• Key requirement for compliance
Row-Level Security
• Filter data dynamically by user
identity
• Implement geographic or
business-unit boundaries
• Supports dynamic SQL predicates
• Enhances zero-trust access
controls
• Important for multi-tenant data
governance
Audit Logging
• Captures all table/column access events
• Stores logs in cloud-native logging systems
• Provides user identity and timestamp for every access
• Supports compliance frameworks (HIPAA, GDPR, SOC)
• Useful for investigation and anomaly detection
Data Sharing Governance
• Control what data can be shared externally
• Granular permissions for recipients
• Audit trails for all sharing actions
• Isolation boundaries with secure sharing
• Supports B2B governed data distribution
Job & Pipeline Governance
• Cluster policies enforce secure compute
• Jobs inherit UC permissions automatically
• Ensure ETL/ML pipelines respect data
boundaries
• Govern execution identities for
automation
• Promotes reproducible governed
workflows
Best Practices for Governance
• Use groups instead of assigning permissions to users
• Create separate catalogs for dev/stage/prod
• Turn on lineage for transparency
• Use volumes instead of DBFS for secure file access
• Perform periodic audits of permissions
Governance Checklist for
Enterprises
• Centralize security using Unity Catalog
• Define access at catalog-level first
• Apply least‑privilege model
• Enable audit logging & monitoring
• Implement automated review cycles