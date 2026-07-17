LAB 4 — Delta Lake Advanced Features: Schema Evolution, Time Travel, OPTIMIZE, and MERGE


Estimated Time: 90 minutes

Objective:

By the end of this lab, learners will:

✔ Use Schema Enforcement & Evolution

✔ Perform Time Travel queries

✔ Use Delta OPTIMIZE & ZORDER

✔ Perform MERGE (CDC) operations

✔ Explore Delta table history



PART A — Setup Delta Table for Lab


Step 1 — Create Base Delta Table
In Databricks, create a new notebook:
Name: Delta_Lake_Advanced_Lab4
Attach to your cluster.
Create a simple table:
data = [(1, "Alice", 50), (2, "Bob", 60)]
df = spark.createDataFrame(data, ["id", "name", "score"])

df.write.format("delta").mode("overwrite").save("/mnt/lab4/base")


Register table:

CREATE TABLE IF NOT EXISTS delta_base
USING delta
LOCATION '/mnt/lab4/base';
View table:

SELECT * FROM delta_base;


PART B — Test Schema Enforcement

Step 2 — Try Writing Incompatible Schema


Create incompatible data:

data2 = [(3, "Charlie", "invalid_score")]
df2 = spark.createDataFrame(data2, ["id", "name", "score"])


Attempt to write:

df2.write.format("delta").mode("append").save("/mnt/lab4/base")
👉 Expect schema enforcement error

Delta prevents bad data from corrupting the table.



PART C — Enable Schema Evolution

Step 3 — Add a New Column
Add "country" column:

df3 = df.withColumn("country", lit("USA"))
Write with schema evolution:

df3.write.format("delta").option("mergeSchema", "true").mode("overwrite").save("/mnt/lab4/base")
Confirm:

DESCRIBE delta_base;


PART D — Delta Time Travel


Step 4 — View Version History
Run:

DESCRIBE HISTORY delta_base;

Step 5 — Query Previous Versions
Query old version:

SELECT * FROM delta_base VERSION AS OF 0;


Compare with latest:

SELECT * FROM delta_base;


PART E — MERGE (Upsert) Operation
Step 6 — Prepare CDC Data


Create update dataset:

changes = [(1, "Alice", 55), (4, "David", 70)]
df_changes = spark.createDataFrame(changes, ["id", "name", "score"])
df_changes.createOrReplaceTempView("changes")

Step 7 — Run MERGE
Execute:

MERGE INTO delta_base AS base
USING changes AS src
ON base.id = src.id
WHEN MATCHED THEN UPDATE SET base.score = src.score
WHEN NOT MATCHED THEN INSERT *;


Validate output:

SELECT * FROM delta_base ORDER BY id;


PART F — Delta OPTIMIZE & ZORDER
Step 8 — Run OPTIMIZE


Optimize files:

OPTIMIZE delta_base;
Step 9 — ZORDER by Column


Improve selective query performance:

OPTIMIZE delta_base ZORDER BY (id);


PART G — VACUUM for File Cleanup

Step 10 — Clean Up Old Versions


Preview:

VACUUM delta_base DRY RUN;


Apply cleanup:

VACUUM delta_base RETAIN 1 HOURS;


Lab 4 Completion Criteria


✔ Performed schema enforcement & evolution

✔ Performed time travel queries

✔ Performed MERGE to simulate CDC

✔ Used OPTIMIZE & ZORDER

✔ Used VACUUM & History to understand versioning