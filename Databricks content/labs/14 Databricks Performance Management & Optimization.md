Databricks Performance Management & Optimization — Complete Hands-On Lab
Duration: 90–120 mins
Difficulty: Intermediate → Advanced
Platforms: Azure Databricks / AWS Databricks
Cluster Runtime: 12.x or later (Photon recommended)

Lab Objectives


By the end of this lab, learners will be able to:

Optimize compute using cluster policies, autoscaling, and Photon.
Apply Delta Lake optimization features (OPTIMIZE, ZORDER, file compaction).
Improve query performance using caching & indexing strategies.
Tune SQL Warehouse and Spark configurations.
Perform cost-efficient transformations.
Monitor workloads using Spark UI, Query History, and Ganglia.
Identify performance bottlenecks and apply best practices.

------------------------------------------
SECTION 1 — Cluster Performance Optimization
------------------------------------------
Step 1.1 — Create an Optimized Cluster
Go to Compute → Create Compute
Choose:
Mode: Single user or Shared
Runtime: Databricks Runtime with Photon
Enable:
Photon Acceleration: ON
Autoscaling: ON
Min workers = 1
Max workers = 8
Set Auto-termination: 10 min
✔ Expected Result: You have a cost-efficient, auto-scaling cluster with Photon.

Step 1.2 — Benchmark Without Photon (Optional)
Turn OFF Photon and compare the same workloads.

Example test:

from pyspark.sql.functions import col, rand

df = spark.range(0, 100_000_000).withColumn("value", rand())

df.groupBy((col("id") % 10).alias("bucket")).count().show()
Measure execution time with:

import time
start = time.time()
df.groupBy((col("id") % 10)).count().collect()
end = time.time()
print("Execution Time:", end-start)
✔ Compare with + without Photon.


------------------------------------------
SECTION 2 — Delta Lake Performance Optimization
------------------------------------------
We will load messy small files, optimize them, and observe improvements.

Step 2.1 — Generate Many Small Files (Anti-Pattern)
df = spark.range(0, 5_000_000)
df.repartition(2000).write.format("delta").mode("overwrite").save("/mnt/data/small_files_delta")
This intentionally writes 2,000 small delta files, slowing down reads.

Step 2.2 — Measure Read Performance (Before OPTIMIZE)
import time
start = time.time()

spark.read.format("delta").load("/mnt/data/small_files_delta").count()

print("Read time BEFORE optimize:", time.time() - start)
Step 2.3 — Compact Files Using OPTIMIZE
Run in SQL:

OPTIMIZE delta.`/mnt/data/small_files_delta`
✔ This compacts small Parquet files into fewer large files.

Step 2.4 — Measure Read Performance (After OPTIMIZE)
start = time.time()

spark.read.format("delta").load("/mnt/data/small_files_delta").count()

print("Read time AFTER optimize:", time.time() - start)
✔ Should be significantly faster.



------------------------------------------
SECTION 3 — Z-ORDER for Query Acceleration
------------------------------------------
Step 3.1 — Create a Delta Table With Common Filter Columns
df = spark.range(0, 50_000_000)\
          .withColumn("category", (col("id") % 20))\
          .withColumn("region", (col("id") % 5))

df.write.format("delta").mode("overwrite").save("/mnt/data/zorder_demo")
Step 3.2 — Read Without ZORDER (Baseline)
start = time.time()
spark.read.format("delta").load("/mnt/data/zorder_demo")\
    .filter("region = 3").count()
print("Baseline time:", time.time() - start)
Step 3.3 — Apply ZORDER
OPTIMIZE delta.`/mnt/data/zorder_demo`
ZORDER BY (region);
Step 3.4 — Read Again (Optimized)
start = time.time()
spark.read.format("delta").load("/mnt/data/zorder_demo")\
    .filter("region = 3").count()
print("After ZORDER time:", time.time() - start)
✔ Expect much faster filter performance.


------------------------------------------
SECTION 4 — Caching Strategies
------------------------------------------
Static datasets should be cached for repeated use.



Step 4.1 — Cache a Table
df = spark.read.format("delta").load("/mnt/data/zorder_demo")
df.cache().count()
Step 4.2 — Measure Query Time (Cached)
start = time.time()
df.filter("category = 5").count()
print("Cached time:", time.time() - start)
✔ Should be instant due to cached memory execution.



Step 4.3 — Clear Cache
CLEAR CACHE;

------------------------------------------
SECTION 5 — SQL Warehouse Performance
------------------------------------------
SQL Warehouses (formerly SQL Endpoints) can be tuned separately.

Step 5.1 — Create a SQL Warehouse
Go to SQL → SQL Warehouses
Create
Starter/Pro/Classic (Starter recommended for lab)
Enable Serverless (if available)
✔ Expected: A running SQL WH instance.

Step 5.2 — Run a Query and Check Query History
SELECT category, COUNT(*) 
FROM delta.`/mnt/data/zorder_demo`
GROUP BY category;
Now open:

SQL → Query History

Observe:

execution time
partitions scanned
parallelism
I/O profile
Step 5.3 — Use Photon Execution Engine
If using Pro/Serverless, Photon is auto-enabled.

Compare Photon On vs Off using large aggregations.


------------------------------------------
SECTION 6 — Job Optimization & Auto-Scaling
------------------------------------------
Step 6.1 — Create a Job
Go to Workflows → Jobs
Create job:
Task: Notebook
Select the current notebook
Cluster mode: Job Compute
Autoscaling: ON
Step 6.2 — Benchmark Job Run Time
Run job → Note execution time.

Now change:

Turn Autoscaling OFF
Set fixed 1 worker
Run again.

✔ Compare performance and stability.


------------------------------------------
SECTION 7 — Advanced Spark Config Optimization
------------------------------------------
These configs can improve performance but should be applied carefully.



Step 7.1 — Enable AQE (Adaptive Query Execution)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
Re-run a heavy query:

spark.read.format("delta").load("/mnt/data/small_files_delta") \
      .groupBy("id").count().count()
Step 7.2 — Enable Broadcast Joins
When joining a small table:

SET spark.sql.autoBroadcastJoinThreshold = 50MB;
Step 7.3 — Skew Handling Example
Identify skew:

SELECT region, COUNT(*) FROM delta.`/mnt/data/zorder_demo` GROUP BY region;
A heavy skew = use AQE or salted joins.



------------------------------------------
SECTION 8 — Troubleshooting with Spark UI
------------------------------------------
Go to Compute → your-cluster → Spark UI
Navigate:
Jobs → identify long-running jobs
Stages → skew, shuffles, long tasks
Storage → check caching
SQL Tab → Query plans

------------------------------------------
SECTION 9 — Performance Lab Summary & Checklist
------------------------------------------
Learners should now know how to:

✔ Optimize clusters using Photon, autoscaling, and instance types

✔ Use Delta Lake optimizations: OPTIMIZE, ZORDER, VACUUM

✔ Reduce file fragmentation and metadata overhead

✔ Use caching effectively

✔ Tune SQL Warehouse workloads

✔ Understand Spark UI for debugging

✔ Enable AQE and broadcast joins

✔ Improve ETL, ML, and streaming performance