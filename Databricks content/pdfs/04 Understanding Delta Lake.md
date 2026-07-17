Lakehouse Architecture Overview
• Explains the unified approach combining
data lake flexibility with warehouse
reliability.
• Describes how Databricks Lakehouse
removes data silos across analytics and
ML.
• Highlights openness through Parquet,
Delta, and cloud object storage
integration.
• Shows how governance, performance,
and cost efficiency are built into the
design.
• Introduces key layers: storage,
governance, compute, and consumption.
• Positions Lakehouse as core foundation
for enterprise-scale workloads.
Why Lakehouse Matters
• Solves challenges of duplicated ETL across warehouses
and lakes.
• Reduces operational overhead by eliminating separate
batch and BI platforms.
• Improves agility by supporting SQL, ML, and streaming
from the same data.
• Provides strong reliability through ACID transactions on
Delta Lake.
• Supports evolution from traditional DW to modern
analytics architecture.
• Enables faster experimentation and deployment with
fewer moving parts.
Role of Delta Lake
• Delta Lake brings reliability with
ACID transactions on large-scale
data.
• Supports schema evolution that
adapts as data sources change
over time.
• Ensures data correctness with
versioning and time travel
capabilities.
• Improves query performance
through intelligent data skipping
and caching.
• Works seamlessly with cloud
object storage for cost-effective
data management.
• Forms the backbone of databricks
Lakehouse implementation.
Delta Lake Storage Format
• Built on Parquet with additional transaction
logs for reliability.
• Provides atomic reads and writes across
distributed cloud storage.
• Supports open protocol enabling
cross-platform data access.
• Stores metadata efficiently for fast table
discovery and optimization.
• Allows scalable columnar processing ideal
for analytics.
• Enables multi-versioned data access using
commit logs.
Delta Transaction Log (_delta_log)
• Records every operation applied to Delta
tables for full auditability.
• Maintains snapshots allowing consistent reads
during writes.
• Contains JSON and checkpoint Parquet files
for fast metadata access.
• Enables time travel by referencing previous
table versions.
• Drives concurrency control ensuring writers
do not conflict.
• Optimizes query planning through recorded
metadata changes.
Delta Time Travel
• Allows users to query past versions of data
using VERSION AS OF syntax.
• Useful for debugging, auditing, or
recovering accidental data changes.
• Enables reproducibility for machine
learning experiments.
• Supports both timestamp-based and
version-number-based access.
• Stores historical files efficiently without
heavy duplication.
• Improves governance by ensuring data
lineage visibility.
Schema Enforcement
• Prevents corrupt or invalid data
from entering tables.
• Ensures column types remain
consistent across writes.
• Rejects incompatible writes to
maintain data integrity.
• Allows defining expectations for
structured datasets.
• Supports production-grade data
pipelines at scale.
• Enhances reliability for downstream
analytics workloads.
Schema Evolution
• Allows adding new columns without breaking existing pipelines.
• Automatically adjusts schemas when new attributes appear.
• Supports user-controlled or auto-evolution modes.
• Useful for rapidly changing source systems such as logs.
• Prevents manual schema migrations for ETL pipelines.
• Improves developer agility in dynamic data environments.
Delta Lake Performance Features
• Leverages data skipping for faster queries by pruning irrelevant files.
• Uses Z-order clustering to optimize column-based filtering.
• Supports caching to reduce compute and IO overhead.
• Includes optimized writes reducing small-file issues.
• Offers auto-compaction via OPTIMIZE commands.
• Improves overall throughput for SQL and ML workloads.
Delta OPTIMIZE
• Reduces small-file fragmentation by rewriting data
groups.
• Improves read performance for large analytical
queries.
• Supports Z-ordering to reorganize data by key
columns.
• Runs as a maintenance task or scheduled job in
production.
• Creates larger, more efficient Parquet files for
querying.
• Essential for long-term Lakehouse performance
stability.
Delta Z-Ordering
• Orders data to colocate related records
physically.
• Improves filtering speed for common query
predicates.
• Reduces IO by enabling more effective data
skipping.
• Works best on high-cardinality columns like
IDs.
• Typically applied during OPTIMIZE
operations.
• Critical for large datasets with frequent
selective queries.
Medallion Architecture Overview
• Describes organizing data into Bronze, Silver,
and Gold layers.
• Bronze contains raw ingested data from
various sources.
• Silver hosts cleaned and structured data for
downstream use.
• Gold contains BI-ready, aggregated, and
curated datasets.
• Improves discoverability and governance of
data workflows.
• Enables modular, scalable ETL design across
teams.
Bronze Layer
• Stores raw ingested data with minimal transformations.
• Acts as immutable source-of-truth for lineage and recovery.
• Supports structured, semi-structured, and unstructured formats.
• Ideal for replaying ETL pipelines when requirements change.
• Often includes incremental ingestion strategies.
• Forms foundation for reliable multi-hop data processing.
Silver Layer
• Applies cleaning, normalization, and conformance rules.
• Ensures data quality for downstream consumers.
• Enforces schema alignment across related datasets.
• Supports joins and enrichment from multiple Bronze sources.
• Provides stable, business-ready tables for analytics.
• Key output source for ML feature engineering as well.
Gold Layer
• Contains aggregated, domain-specific, analytics-ready tables.
• Supports BI dashboards, reporting, and KPIs.
• Often shaped around business domains such as finance or sales.
• Includes transformations that align with stakeholder needs.
• Optimized for high concurrency SQL workloads.
• Final layer consumed by analysts and business users.
Delta Table Types
• Managed tables store data under
Databricks workspace paths.
• External tables reference cloud object
storage locations.
• Managed tables simplify lifecycle
management automatically.
• External tables provide greater control
for shared environments.
• Choice depends on governance, data
ownership, and organization policies.
• Both support full Delta Lake ACID and
schema capabilities.
Creating Delta Tables
• Can be created via SQL DDL, DataFrame writes, or UI interfaces.
• Supports CREATE TABLE AS SELECT (CTAS) operations.
• Allows specifying partitioning strategy for large tables.
• Can load from Parquet, CSV, JSON, or other formats.
• Supports evolving schemas during writes when enabled.
• Makes onboarding new datasets simple and scalable.
Partitioning Strategy
• Improves performance by pruning
partitions during queries.
• Should align with common filtering
patterns such as dates.
• Over-partitioning can cause small-file
inefficiencies.
• Under-partitioning can slow down
large-table scanning.
• Delta OPTIMIZE helps fix partitioning
imbalance issues.
• Critical tuning step for Lakehouse
performance.
Streaming with Delta
• Delta supports both streaming sources and sinks using Structured Streaming.
• Allows incremental processing directly into Delta tables.
• Provides exactly-once guarantees for reliable stream ingestion.
• Unifies batch and streaming into a single pipeline model.
• Supports restartability through checkpointing.
• Ideal for real-time analytics and ingestion workloads.
Batch vs Streaming Delta
Workloads
• Batch loads large amounts of data at
scheduled intervals.
• Streaming ingests records continuously as
events arrive.
• Delta supports mixing both modes on
shared tables.
• Batch and streaming pipelines can be
unified in Medallion flows.
• Ensures flexibility depending on data
arrival patterns.
• Facilitates modern near–real-time
architecture needs.
Concurrency Control
• Delta ensures serializable isolation across concurrent writers.
• Handles overlapping operations gracefully using optimistic concurrency.
• Prevents readers from seeing partial writes during updates.
• Uses checkpointing to improve metadata access speed.
• Allows many users to read while pipelines write.
• Essential for multi-team enterprise Lakehouse usage.
Delta MERGE Operations
• Supports upserts combining insert, update,
and delete logic.
• Useful for CDC, SCD, and system-of-record
datasets.
• Allows matching source and target rows
based on business keys.
• Reduces pipeline complexity compared to
multi-step ETL.
• Executes efficiently using Delta's
transaction log.
• Core operation for production-grade data
warehousing tasks.
Delta Vacuum
• Removes obsolete historical files to
free storage space.
• Used to manage retention window
for time travel history.
• Ensures compliance with cloud
storage cost optimization.
• Must be used carefully to avoid
losing required versions.
• Supports dry-run mode to preview
which files will be removed.
• Critical maintenance task for
long-running Delta tables.
Governance in the Lakehouse
• Unity Catalog integrates governance
across tables, views, and files.
• Provides centralized permission
management for all data assets.
• Tracks data lineage from raw to curated
layers.
• Ensures consistent auditing across
multiple workspaces.
• Supports tokenized and role-based
policies for secure access.
• Completes Lakehouse architecture with
end-to-end governance.
Lakehouse Summary & Benefits
• Combines best elements of data lakes and data warehouses.
• Delta Lake powers reliability, performance, and usability.
• Medallion architecture structures data engineering pipelines effectively.
• Supports unified batch, streaming, ML, and BI workloads.
• Provides open, scalable, cloud-native foundation for analytics.
• Enables organizations to modernize and accelerate data strategy.