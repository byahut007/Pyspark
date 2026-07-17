Assignment Overview


This assignment validates your understanding of:

Databricks Workspace navigation
Cluster setup and validation
DBFS file operations
Uploading, copying, moving, deleting files
Reading & writing data using Spark
Notebook documentation
SQL + Python execution
Basic governance concepts
You must complete all tasks inside a Databricks Notebook and use ONLY DBFS paths.



Learning Outcomes


By completing this assignment, you will demonstrate:

Ability to work within the Databricks workspace
Understanding of clusters and execution environments
Proficiency in DBFS commands (ls, cp, mv, rm, mkdirs)
Ability to handle CSV ingestion and transformation
Skill in writing outputs in JSON, Parquet, and Delta formats
Ability to run Python + SQL cells in a unified notebook
Proper documentation using markdown
--------------------------------------------------------------
SECTION A — Workspace & Notebook Setup
--------------------------------------------------------------
Task A1 — Create Folder
Inside your user workspace, create:

assignment_dbfs_lld
Task A2 — Create Notebook
Notebook name must be:

dbfs_mastery_assignment
Default language: Python

Task A3 — Attach Cluster
Attach an active cluster.

Add a cell that prints cluster name:

spark.conf.get("spark.databricks.clusterUsageTags.clusterName")
--------------------------------------------------------------
SECTION B — DBFS Folder Structure
--------------------------------------------------------------
Create the following directory structure using dbutils.fs.mkdirs() only:

dbfs:/mnt/learnlytica/
    ├── input/
    ├── processed/
    ├── archive/
    └── logs/
--------------------------------------------------------------
SECTION C — File Upload & DBFS Operations
--------------------------------------------------------------
Task C1 — Upload File
Upload students.csv into:

dbfs:/mnt/learnlytica/input/students.csv
Use this sample CSV:

id,name,age,score
1,Asha,21,87
2,Rohan,23,92
3,Meera,22,78
4,Vinod,24,80
Task C2 — Demonstrate DBFS Commands
Add code cells showing the following:

List (ls)
dbutils.fs.ls("dbfs:/mnt/learnlytica/input")
Copy (cp)
dbutils.fs.cp("dbfs:/mnt/learnlytica/input/students.csv",
              "dbfs:/mnt/learnlytica/archive/students_backup.csv")
Move (mv)
Move the backup file back into input:

dbutils.fs.mv("dbfs:/mnt/learnlytica/archive/students_backup.csv",
              "dbfs:/mnt/learnlytica/input/students_backup.csv")
Delete (rm)
Delete the logs folder:

dbutils.fs.rm("dbfs:/mnt/learnlytica/logs", True)
⚠️ Deleting must be recursive.
--------------------------------------------------------------
SECTION D — Reading & Transforming Data
--------------------------------------------------------------
Task D1 — Load CSV using Spark
df = spark.read.csv("dbfs:/mnt/learnlytica/input/students.csv",
                    header=True,
                    inferSchema=True)
df.show()
Task D2 — Transform the Data
Perform ALL of the following:

Filter students with score > 80
Create new column "passed" (boolean)
Calculate average score
Show top 3 students by score
Example:

from pyspark.sql.functions import col, avg

df2 = df.filter(col("score") > 80)
df2 = df2.withColumn("passed", col("score") > 80)
df2.show()
--------------------------------------------------------------
SECTION E — Writing Output Files
--------------------------------------------------------------
Write the transformed data to three formats:

E1 — Write JSON
dbfs:/mnt/learnlytica/processed/students_json/
E2 — Write Parquet
dbfs:/mnt/learnlytica/processed/students_parquet/
E3 — Write Delta
dbfs:/mnt/learnlytica/processed/students_delta/
Example:

df2.write.mode("overwrite").json("dbfs:/mnt/learnlytica/processed/students_json")
--------------------------------------------------------------
SECTION F — SQL Execution
--------------------------------------------------------------
Task F1 — Register Temp Table
df.createOrReplaceTempView("students_tbl")
Task F2 — Run SQL Query
%sql
SELECT name, score
FROM students_tbl
WHERE score > 85;
--------------------------------------------------------------
SECTION G — Notebook Documentation
--------------------------------------------------------------
Your notebook must include:

Markdown headers (#, ##, ###)
Explanation of each step
Why you created each DBFS directory
Screenshot (optional) of DBFS folder view
Comments in code cells