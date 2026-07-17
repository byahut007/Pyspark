Performance Optimization in
Databricks Overview
• Introduces strategies to maximize
cluster and query performance.
• Explains how Spark, Delta Lake, and
Photon influence speed.
• Shows why performance tuning is
essential for large datasets.
• Highlights common bottlenecks such
as shuffles and skew.
• Prepares learners for advanced
Databricks optimization workflows.
• Foundation for scaling analytics and
ETL pipelines.
Understanding Spark Execution
Model
• Spark uses distributed computation
across worker nodes.
• Jobs contain stages, and stages
contain parallel tasks.
• Shuffle operations occur when data
moves across nodes.
• Understanding DAGs helps identify
performance bottlenecks.
• Spark UI provides visibility into
execution flow.
• Key to optimizing transformations
and data movement.
Cluster Sizing Strategies
• Choose driver and worker sizes
based on workload patterns.
• Larger memory helps with caching
and joins.
• CPU-heavy workloads need more
vCPUs per node.
• Autoscaling adjusts nodes
dynamically to demand.
• Job clusters reduce cost for
scheduled workloads.
• Right-sizing prevents
underperformance and
overspending.
Photon Execution Engine
• Photon is a next-gen vectorized engine
for SQL workloads.
• Boosts performance for scans, filters,
joins, and aggregations.
• Compatible with Delta Lake and SQL
warehouse operations.
• Reduces CPU usage through optimized
vector processing.
• Transparent to users—no code changes
required.
• Recommended for high-volume
analytical pipelines.
Adaptive Query Execution (AQE)
• AQE dynamically optimizes queries
during runtime.
• Handles skewed joins by splitting
large partitions.
• Optimizes shuffle partitions based on
statistics.
• Supports dynamic switching of join
strategies.
• Improves stability for unpredictable
data distributions.
• Enabled by default in modern
Databricks runtimes.
Optimizing Joins
• Broadcast joins improve
performance for small dimension
tables.
• Shuffle joins used when both tables
are large.
• Skewed joins require salting or AQE
adjustments.
• Partitioning strategy influences join
speed significantly.
• Check Spark UI to understand join
behavior.
• Selecting correct join type is key to
optimization.
Data Skew Mitigation
• Skew occurs when partitions have uneven
numbers of rows.
• Can cause long-running tasks and incomplete
jobs.
• Salting distributes values more evenly across
partitions.
• AQE automatically handles skewed joins in
many cases.
• Custom partitioning helps address severe
skew.
• Essential for stable pipeline performance.
Caching & Persistence
• Cache hot DataFrames for repeated
transformations.
• Persist allows selecting memory/disk
level for storage.
• Improves iterative workload
performance significantly.
• Over-caching can increase memory
pressure on cluster.
• Use unpersist() to clean unused
caches.
• Best applied to intermediate
reusable datasets.
Partitioning Best Practices
• Partition by frequently filtered columns
for efficient pruning.
• Avoid over-partitioning to prevent
small-file inefficiencies.
• Use OPTIMIZE to compact files for
consistent partition layout.
• Partitioning impacts both read and write
performance.
• Choose partition keys based on query
patterns.
• Critical for large-scale production
datasets.
Z-Ordering for Performance
• Physically organizes data to colocate related rows.
• Improves filtering and lookup speed for selective queries.
• Reduces IO and accelerates analytical semantics.
• Frequently used on high-cardinality columns like IDs.
• Applied as part of the OPTIMIZE command.
• Major performance win for large Delta tables.
Small File Optimization
• Small files degrade performance due to metadata overhead.
• OPTIMIZE rewrites many small files into larger ones.
• Auto Loader helps manage file sizes at ingestion time.
• Delta compaction processes maintain long-term efficiency.
• Partitioning strategy influences small file generation.
• Essential to address especially in streaming scenarios.
Delta Lake OPTIMIZE
• Consolidates many small files into optimized Parquet files.
• Improves read-heavy workloads dramatically.
• Z-ordering enhances sort-based optimizations.
• Can be scheduled regularly for maintenance.
• Reduces metadata load on the execution engine.
• Key for high-performance Lakehouse environments.
Delta Caching
• Stores frequently accessed data on
cluster SSDs.
• Accelerates repetitive scans and BI
workloads.
• Useful for Gold layer analytics with
high concurrency.
• Activated automatically in several
cluster types.
• Reduces need to re-read data from
cloud storage.
• Improves CPU utilization efficiency.
SQL Warehouse Performance
• Warehouses provide fully managed
compute for BI workloads.
• Scaling levels handle varying
dashboard concurrency.
• Photon engine boosts SQL execution
speed.
• Warehouse history shows query
performance trends.
• Materialized views accelerate
repeated query patterns.
• Best suited for analysts running
SQL-based dashboards.
Shuffle Optimization
• Shuffles occur when Spark redistributes data across workers.
• Large shuffles create heavy network and disk IO.
• Reduce shuffles by avoiding wide transformations.
• Broadcast joins often eliminate shuffle needs.
• Repartition intelligently to reduce shuffle stages.
• Shuffle UI helps diagnose heavy operations.
Repartitioning Techniques
• repartition() redistributes data evenly but
triggers shuffle.
• coalesce() reduces partitions without
shuffle overhead.
• Optimize partition count based on cluster
size.
• Over-partitioning causes unnecessary
scheduling overhead.
• Under-partitioning reduces parallelism.
• Balancing partition count is key to speed.
Optimizing UDF Usage
• UDFs can be slower than native Spark functions.
• Use built-in functions whenever possible.
• Pandas UDFs perform better for vectorized workloads.
• Avoid Python UDFs inside large transformations.
• Scala UDFs may offer better performance.
• Rewriting UDF logic in SQL often yields improvements.
Handling Large Tables Efficiently
• Use partition pruning to limit scan range.
• Apply Z-ordering for highly selective filters.
• Optimize tables regularly for sustained performance.
• Use Delta caching for frequent table access.
• Cluster selection influences scan speed.
• Monitor access patterns to refine optimization steps.
Streaming Performance Tuning
• Checkpointing ensures recoverability and reduces recomputation.
• Trigger intervals control event processing speed.
• Auto Loader helps optimize incremental ingestion.
• Watermarks prevent unbounded state growth.
• Optimize sink tables regularly to prevent small files.
• Streaming jobs must be monitored for latency and throughput.
Photon for ETL Pipelines
• Photon accelerates SQL transformations
dramatically.
• Suitable for heavy aggregation and
filtering workloads.
• Compatible with Delta Lake ETL pipelines.
• Requires no code changes for Spark SQL.
• Improves cost efficiency by reducing
compute time.
• Recommended for enterprise-scale
transformations.
Cluster Configuration Optimization
• Choose worker type based on memory or CPU requirements.
• Autoscaling helps handle spikes in workload demand.
• Spot instances reduce cost while maintaining performance.
• Enable IO-optimized instances for heavy Delta workloads.
• Use pool clusters to reduce startup latency.
• Review cluster logs for configuration guidance.
Monitoring Spark Jobs
• Spark UI exposes execution plan and bottleneck details.
• Task timelines identify skew and long-running tasks.
• Storage UI shows cached DataFrame sizes.
• SQL tab reveals query execution breakdown.
• Logs provide granular debug-level insights.
• Monitoring is essential for ongoing tuning.
Explaining Query Plans
• EXPLAIN shows physical and logical plans.
• Helps identify unnecessary shuffles or scans.
• Reveals if broadcast joins are being used.
• Displays partition pruning effectiveness.
• Guides developer decisions for rewriting queries.
• Important step in SQL and DataFrame optimization.
Performance Testing &
Benchmarking
• Benchmark ETL workloads under realistic data volumes.
• Compare runtimes with optimized vs non-optimized tables.
• Use cluster metrics to guide tuning.
• A/B test partitioning and Z-order strategies.
• Use SQL warehouse history for long-term insights.
• Validate improvements before production rollout.
Performance Optimization
Summary
• Focus on reducing shuffles, skew, and small files.
• Use Delta OPTIMIZE, Z-ordering, and caching effectively.
• Right-size clusters and leverage Photon engine.
• Continuously monitor Spark UI for bottlenecks.
• Apply partitioning strategies aligned with access patterns.
• Performance tuning is ongoing—not one-time.