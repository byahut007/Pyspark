Lab: Delta Lake Transformations End-to-End on Databricks

Duration
90–120 minutes (can be split into 2 labs)


Learning Objectives
By the end of this lab, learners will be able to:

Create and write Delta tables from Spark DataFrames.
Perform UPDATE, DELETE, and MERGE (upsert) operations.
Implement Slowly Changing Dimensions (SCD Type 1 & Type 2) using Delta Lake.
Use schema evolution and understand its impact.
Query historical versions using time travel.
Improve performance using OPTIMIZE and Z-ORDER.
Use VACUUM for cleanup and understand its risks.
Implement a simple Bronze → Silver → Gold pipeline.

0. Prerequisites


A Databricks workspace (Community Edition or Azure Databricks).
A running cluster (Runtime 12.x or later recommended).
Basic familiarity with Spark DataFrames and SQL.
Note: All examples below are shown in PySpark and some in SQL. You can choose one style or mix both.

1. Lab Setup – Notebook & Paths


Step 1.1 – Create a Notebook
In the left sidebar, click Workspace.
Navigate to your user folder (e.g., Users/your.email@domain.com).
Click ▼ next to your folder → Create → Notebook.
Name it: delta_transformations_lab.
Choose Default Language: Python.
Click Create.
Step 1.2 – Attach Cluster
At the top of the notebook, from Cluster dropdown, choose your running cluster.
Wait for the status to show Attached.
Step 1.3 – Set Base Paths
In the first cell, run:

base_path = "dbfs:/tmp/delta_transformations_lab"  # you can change prefix
dim_customers_path = f"{base_path}/dim_customers"
fact_orders_path = f"{base_path}/fact_orders"
bronze_path = f"{base_path}/bronze"
silver_path = f"{base_path}/silver"
gold_path = f"{base_path}/gold"

base_path, dim_customers_path, fact_orders_path
This defines reusable paths for all later steps.


2. Create & Write Initial Delta Table


We’ll start with a simple customers dimension table.

Step 2.1 – Create Initial DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

data_customers = [
    (1, "Alice",  "Gold",  "US"),
    (2, "Bob",    "Silver","US"),
    (3, "Charlie","Bronze","UK"),
    (4, "Diana",  "Gold",  "DE")
]

schema_customers = StructType([
    StructField("customer_id", IntegerType(), False),
    StructField("customer_name", StringType(), True),
    StructField("loyalty_tier", StringType(), True),
    StructField("country", StringType(), True)
])

df_customers = spark.createDataFrame(data_customers, schema_customers)
df_customers.show()
df_customers.printSchema()
Verify:

4 rows.
Columns: customer_id, customer_name, loyalty_tier, country.
Step 2.2 – Write as a Delta Table (Initial Write)
df_customers.write.format("delta") \
    .mode("overwrite") \
    .save(dim_customers_path)
Step 2.3 – Register as a Managed Table (Optional but Recommended)
spark.sql(f"DROP TABLE IF EXISTS dim_customers_delta")
spark.sql(f"CREATE TABLE dim_customers_delta USING DELTA LOCATION '{dim_customers_path}'")
Check content via SQL:

%sql
SELECT * FROM dim_customers_delta;
You now have a Delta table ready for transformations.


3. UPDATE Transformations


Let’s correct wrong loyalty tiers.

Step 3.1 – Identify Records to Update
%sql
SELECT * FROM dim_customers_delta WHERE customer_name = 'Charlie';
Step 3.2 – Run UPDATE
%sql
UPDATE dim_customers_delta
SET loyalty_tier = 'Silver'
WHERE customer_name = 'Charlie';
Step 3.3 – Verify Update
%sql
SELECT * FROM dim_customers_delta;
Expected:

Charlie now has loyalty_tier = Silver.

4. DELETE Transformations


Remove customers from a specific country (e.g., DE).

Step 4.1 – Check Data
%sql
SELECT * FROM dim_customers_delta WHERE country = 'DE';
Step 4.2 – DELETE Rows
%sql
DELETE FROM dim_customers_delta
WHERE country = 'DE';
Step 4.3 – Verify
%sql
SELECT * FROM dim_customers_delta;
Diana (DE) should be removed.

Note: Physically, files still exist until VACUUM is executed later.

5. MERGE INTO – Upserts (CDC-Style)


Simulate a small Change Data Capture (CDC) batch.

Step 5.1 – Create a Source DataFrame with Changes
cdc_data = [
    # Existing customer with changed tier
    (1, "Alice",  "Platinum", "US"),
    # Existing customer with updated country
    (2, "Bob",    "Silver",   "CA"),
    # New customer
    (5, "Ellen",  "Bronze",   "FR")
]

df_cdc = spark.createDataFrame(cdc_data, schema_customers)
df_cdc.show()
Step 5.2 – Perform MERGE (Upsert)
%sql
MERGE INTO dim_customers_delta AS tgt
USING (
  SELECT 1 AS customer_id, 'Alice' AS customer_name, 'Platinum' AS loyalty_tier, 'US' AS country UNION ALL
  SELECT 2, 'Bob', 'Silver', 'CA' UNION ALL
  SELECT 5, 'Ellen', 'Bronze', 'FR'
) AS src
ON tgt.customer_id = src.customer_id
WHEN MATCHED THEN
  UPDATE SET
    tgt.customer_name = src.customer_name,
    tgt.loyalty_tier  = src.loyalty_tier,
    tgt.country       = src.country
WHEN NOT MATCHED THEN
  INSERT (customer_id, customer_name, loyalty_tier, country)
  VALUES (src.customer_id, src.customer_name, src.loyalty_tier, src.country);
Step 5.3 – Verify MERGE
%sql
SELECT * FROM dim_customers_delta ORDER BY customer_id;
Expected:

Alice updated to Platinum.
Bob’s country updated to CA.
Ellen (5) inserted as a new row.

6. SCD Type 1 with Delta Lake


In SCD Type 1, we overwrite current values and do not maintain history.

You actually already implemented SCD1 style in the previous MERGE (just update in place).

To explicitly frame it:

Step 6.1 – Another SCD1 Update
%sql
MERGE INTO dim_customers_delta AS tgt
USING (
  SELECT 2 AS customer_id, 'Bob', 'Gold', 'CA'
) AS src
ON tgt.customer_id = src.customer_id
WHEN MATCHED THEN
  UPDATE SET
    tgt.loyalty_tier = src.loyalty_tier;
Step 6.2 – Verify
%sql
SELECT * FROM dim_customers_delta WHERE customer_id = 2;
Bob should now be Gold.



7. SCD Type 2 with Delta Lake


Now we’ll maintain history using valid_from, valid_to, and is_current flags.

Step 7.1 – Create SCD2 Table from Scratch
Drop old table and recreate as SCD2:

%sql
DROP TABLE IF EXISTS dim_customers_scd2;

from pyspark.sql.functions import current_timestamp, lit

df_scd2 = df_customers \
    .withColumn("valid_from", current_timestamp()) \
    .withColumn("valid_to", lit(None).cast("timestamp")) \
    .withColumn("is_current", lit(True))

df_scd2.write.format("delta").mode("overwrite").save(f"{base_path}/dim_customers_scd2")
spark.sql(f"CREATE TABLE dim_customers_scd2 USING DELTA LOCATION '{base_path}/dim_customers_scd2'")
Step 7.2 – Simulate a Loyalty Tier Change (SCD2)
Suppose Alice changes from Gold → Platinum.

%sql
MERGE INTO dim_customers_scd2 AS tgt
USING (
  SELECT 1 AS customer_id, 'Alice' AS customer_name, 'Platinum' AS loyalty_tier, 'US' AS country
) AS src
ON tgt.customer_id = src.customer_id AND tgt.is_current = TRUE
WHEN MATCHED THEN
  UPDATE SET
    tgt.valid_to   = current_timestamp(),
    tgt.is_current = FALSE
WHEN NOT MATCHED THEN
  INSERT (customer_id, customer_name, loyalty_tier, country, valid_from, valid_to, is_current)
  VALUES (src.customer_id, src.customer_name, src.loyalty_tier, src.country, current_timestamp(), NULL, TRUE);
Note: The trick is to use two MERGE branches – here we used a pattern where the UPDATE closes old record and a new INSERT is triggered via NOT MATCHED. Another variant: use a staging table with both updated and new rows.
Step 7.3 – Verify SCD2 History
%sql
SELECT * FROM dim_customers_scd2
WHERE customer_name = 'Alice'
ORDER BY valid_from;
Expected:

One row with Gold, is_current = false, valid_to NOT NULL.
One row with Platinum, is_current = true, valid_to = NULL.

8. Schema Evolution


We’ll add a new column email into the table automatically.

Step 8.1 – Create New Data with Extra Column
data_new_customers = [
    (6, "Frank", "Silver", "US", "frank@example.com"),
    (7, "Grace", "Gold",   "UK", "grace@example.com")
]

schema_new = StructType([
    StructField("customer_id", IntegerType(), False),
    StructField("customer_name", StringType(), True),
    StructField("loyalty_tier", StringType(), True),
    StructField("country", StringType(), True),
    StructField("email", StringType(), True)
])

df_new = spark.createDataFrame(data_new_customers, schema_new)
df_new.show()
Step 8.2 – Write with mergeSchema Enabled
df_new.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save(dim_customers_path)  # same path as original table
Step 8.3 – Verify Schema Evolution
%sql
DESCRIBE TABLE dim_customers_delta;
You should now see an email column.

Query data:

%sql
SELECT * FROM dim_customers_delta ORDER BY customer_id;
Older rows will have NULL for email.



9. Time Travel


Now we’ll use Delta’s version history.

Step 9.1 – View Table History
%sql
DESCRIBE HISTORY dim_customers_delta;
Note the version column and timestamps.

Step 9.2 – Query an Older Version
Replace <version_number> with a real value from the history:

%sql
SELECT * FROM dim_customers_delta VERSION AS OF <version_number>;
OR using timestamp:

%sql
SELECT * FROM dim_customers_delta TIMESTAMP AS OF '2025-11-18T10:00:00Z'
(Use an actual timestamp from your history output.)


10.OPTIMIZE & Z-ORDER (If Available)


Note: OPTIMIZE and ZORDER BY are available in some Databricks editions and may require Unity Catalog / Premium tier. If unavailable, treat this as conceptual.
Step 10.1 – Run OPTIMIZE
%sql
OPTIMIZE dim_customers_delta;
This compacts small files into fewer large files.



Step 10.2 – Z-ORDER by Column
%sql
OPTIMIZE dim_customers_delta
ZORDER BY (country);
Now queries filtering by country should be faster due to improved data skipping.



11. Streaming Transformations with Delta


We’ll simulate a simple streaming input and write to Delta.

Step 11.1 – Create a Streaming Source (Auto Loader or rate source)
For a simple demo, use Spark’s rate source (no external files):

stream_df = (spark.readStream
    .format("rate")
    .option("rowsPerSecond", 5)
    .load()
    .withColumn("id", F.col("value"))
    .withColumn("event_time", F.col("timestamp"))
    .drop("value", "timestamp")
)

stream_df.printSchema()
Step 11.2 – Write Stream to Delta
stream_output_path = f"{base_path}/stream_delta"

query = (stream_df
    .writeStream
    .format("delta")
    .option("checkpointLocation", f"{base_path}/stream_delta_chk")
    .outputMode("append")
    .start(stream_output_path)
)
Let it run for 30–60 seconds.



Step 11.3 – Read the Streamed Delta Table
stream_delta_df = spark.read.format("delta").load(stream_output_path)
stream_delta_df.show(10)
Stop the stream:

query.stop()
Now you’ve used Delta for streaming.


12. VACUUM – Cleaning Up Files


Important: Learn the concept & risk before running.

Delta keeps old data files for retention period (default 7 days or more). VACUUM physically removes them.

Step 12.1 – Check Current Table History Again
%sql
DESCRIBE HISTORY dim_customers_delta;
Step 12.2 – VACUUM with Default Retention
%sql
VACUUM dim_customers_delta;
For demos some people use VACUUM ... RETAIN 0 HOURS, but this can break time travel and may be disallowed in production. Use only in controlled demo environments if retention config allows.

13. Bronze → Silver → Gold Mini Pipeline


We’ll simulate a simple Medallion architecture.

Step 13.1 – Create Raw Bronze Data
bronze_data = [
    (1, "2025-11-18", "Laptop",  1200.0, "US"),
    (2, "2025-11-18", "Mouse",   25.0,   "US"),
    (3, "2025-11-18", "Keyboard",45.0,   "UK"),
    (4, "2025-11-18", "Monitor", 300.0,  "DE"),
    (5, "2025-11-19", "Laptop",  1300.0, "US")
]

schema_orders = StructType([
    StructField("order_id", IntegerType(), False),
    StructField("order_date", StringType(), True),
    StructField("product", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("country", StringType(), True)
])

df_bronze = spark.createDataFrame(bronze_data, schema_orders)
df_bronze.show()
Write Bronze:

df_bronze.write.format("delta").mode("overwrite").save(bronze_path)
Step 13.2 – Silver: Clean & Cast Types
Convert order_date to proper date, filter invalid rows.

df_silver = (spark.read.format("delta").load(bronze_path)
    .withColumn("order_date", F.to_date("order_date", "yyyy-MM-dd"))
    .filter(F.col("amount") > 0)  # remove invalid/negative amounts
)

df_silver.show()
df_silver.write.format("delta").mode("overwrite").save(silver_path)
Step 13.3 – Gold: Aggregate Revenue per Country
df_gold = (spark.read.format("delta").load(silver_path)
    .groupBy("country")
    .agg(F.sum("amount").alias("total_revenue"))
)

df_gold.show()
df_gold.write.format("delta").mode("overwrite").save(gold_path)
You’ve now demonstrated the full:

Bronze (raw) → Silver (clean) → Gold (aggregated) pipeline using Delta.

14. Lab Checklist & Reflection


At the end, ask learners to confirm they have:

 Created and written a Delta table.
 Performed UPDATE on Delta.
 Performed DELETE on Delta.
 Implemented MERGE for upserts.
 Modeled SCD Type 1 (overwrite).
 Modeled SCD Type 2 (history tracking).
 Used schema evolution with mergeSchema.
 Queried previous versions via time travel.
 Seen or discussed OPTIMIZE and Z-ORDER.
 Written a streaming Delta sink.
 Run VACUUM (conceptually or practically).
 Built a Bronze → Silver → Gold flow.