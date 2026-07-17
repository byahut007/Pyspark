Assignment: Delta Lake Mastery & Lakehouse Patterns
Assignment Code: DATABRICKS-DELTA-ASSIGNMENT-02
Estimated Duration: 90–120 minutes
📝 Assignment Overview
In this assignment, you will work with Delta Lake end-to-end:

Create Delta tables
Perform updates, deletes, merges
Apply SCD Type 1 and Type 2
Use schema evolution
Explore Delta time travel
Understand OPTIMIZE, ZORDER, VACUUM
Build a Bronze → Silver → Gold pipeline
Write to Delta using Structured Streaming
This assignment validates your understanding of real-world Delta Lake features used in enterprise data engineering.

--------------------------------------------------------------
📌 SECTION A — Setup & Folder Structure
--------------------------------------------------------------
Task A1 — Create DBFS Folder Structure
Create the following directories:

dbfs:/mnt/delta_assignment/
    ├── bronze/
    ├── silver/
    ├── gold/
    ├── checkpoints/
    └── logs/
Use:

dbutils.fs.mkdirs("dbfs:/mnt/delta_assignment/bronze")
Repeat for all folders.



--------------------------------------------------------------
📌 SECTION B — Create Initial Delta Table
--------------------------------------------------------------
Task B1 — Create Initial DataFrame
Use this sample JSON data:

data = [
  {"id": 1, "name": "Asha", "city": "Pune",    "score": 88},
  {"id": 2, "name": "Rohan","city": "Mumbai",  "score": 92},
  {"id": 3, "name": "Meera","city": "Delhi",   "score": 78}
]
df = spark.createDataFrame(data)
Task B2 — Write Delta Table
Write to:

dbfs:/mnt/delta_assignment/bronze/students_delta

df.write.format("delta").mode("overwrite").save("dbfs:/mnt/delta_assignment/bronze/students_delta")
Task B3 — Read Back the Table
df_bronze = spark.read.format("delta").load("dbfs:/mnt/delta_assignment/bronze/students_delta")
df_bronze.show()
--------------------------------------------------------------
📌 SECTION C — Perform UPDATE, DELETE, MERGE
--------------------------------------------------------------
Task C1 — UPDATE Delta Table
Increase all scores by +2:

spark.sql("""
UPDATE delta.`dbfs:/mnt/delta_assignment/bronze/students_delta`
SET score = score + 2
""")
Task C2 — DELETE from Delta Table
Delete students with score < 80:

spark.sql("""
DELETE FROM delta.`dbfs:/mnt/delta_assignment/bronze/students_delta`
WHERE score < 80
""")
Task C3 — MERGE Into Delta (Upsert)
New incoming data:

updates = [
  {"id": 2, "name": "Rohan", "city": "Banglore", "score": 95},
  {"id": 4, "name": "Neha",  "city": "Chennai",  "score": 85}
]
df_updates = spark.createDataFrame(updates)
Perform MERGE:

from delta.tables import DeltaTable

deltaTable = DeltaTable.forPath(spark, "dbfs:/mnt/delta_assignment/bronze/students_delta")

deltaTable.alias("t").merge(
    df_updates.alias("s"),
    "t.id = s.id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()
--------------------------------------------------------------
📌 SECTION D — SCD Type 1 (Overwrite Changes)
--------------------------------------------------------------
Apply an SCD Type 1 overwrite rule:

If student exists → overwrite fields
If not → insert
Use MERGE same as above but with business logic explained in markdown.

You MUST:

Document the SCD Type 1 concept
Show before & after screenshots or show()
--------------------------------------------------------------
📌 SECTION E — SCD Type 2 (History Tracking)
--------------------------------------------------------------
Task E1 — Prepare Data with Change
Incoming change:

history_data = [
  {"id": 1, "name": "Asha", "city": "Bangalore", "score": 90}
]
df_history = spark.createDataFrame(history_data)
Task E2 — Implement Type 2 Logic
Your Type 2 table MUST include:

id
name
city
score
start_date
end_date
is_current
You must:

Set previous record is_current = false
Insert new record with is_current = true
Update end_date for old record
Use MERGE with conditional insert/update logic
(Hint: use spark.sql or Delta merge with WHEN MATCHED AND logic.)



--------------------------------------------------------------
📌 SECTION F — Schema Evolution
--------------------------------------------------------------
Add a new column: "email".

Incoming data:

schema_update = [
  {"id": 5, "name": "Kiran", "city": "Hyd", "score": 84, "email": "kiran@example.com"}
]
df_schema = spark.createDataFrame(schema_update)
Write with mergeSchema:

df_schema.write.format("delta") \
  .option("mergeSchema", "true") \
  .mode("append") \
  .save("dbfs:/mnt/delta_assignment/bronze/students_delta")
--------------------------------------------------------------
📌 SECTION G — Time Travel Query
--------------------------------------------------------------
Query an older version:

spark.read.format("delta").option("versionAsOf", 0).load("dbfs:/mnt/delta_assignment/bronze/students_delta").show()
Also run:

spark.sql("DESCRIBE HISTORY delta.`dbfs:/mnt/delta_assignment/bronze/students_delta`")
--------------------------------------------------------------
📌 SECTION H — OPTIMIZE, ZORDER & VACUUM Discussion
--------------------------------------------------------------
Write markdown explaining:
Why OPTIMIZE is needed
How Z-ORDER improves pruning
Why VACUUM removes old files
Retention period considerations
Optional (Azure only):

OPTIMIZE delta.`dbfs:/mnt/...` ZORDER BY (id);
VACUUM delta.`dbfs:/mnt/...` RETAIN 168 HOURS;
--------------------------------------------------------------
📌 SECTION I — Streaming Delta Sink
--------------------------------------------------------------
Write streaming data into Bronze:

Task I1 — Create streaming source
Use rate generator:

stream_df = (
    spark.readStream
         .format("rate")
         .option("rowsPerSecond", 5)
         .load()
)
Task I2 — Write to Delta sink
query = (
    stream_df.writeStream
        .format("delta")
        .option("checkpointLocation", "dbfs:/mnt/delta_assignment/checkpoints/rate_stream")
        .outputMode("append")
        .start("dbfs:/mnt/delta_assignment/bronze/rate_stream_data")
)
Run for 10–20 seconds then stop:

query.stop()
--------------------------------------------------------------
📌 SECTION J — Bronze → Silver → Gold
--------------------------------------------------------------
Task J1 — Bronze Layer
Raw data (already stored in Bronze).

Task J2 — Silver Layer
Clean/standardized form:

Remove nulls
Standardize city names
Convert names to Proper Case
Write to:

dbfs:/mnt/delta_assignment/silver/students_silver
Task J3 — Gold Layer
Analytics table:

Top scoring students
City-wise average score
Write to:

dbfs:/mnt/delta_assignment/gold/students_gold