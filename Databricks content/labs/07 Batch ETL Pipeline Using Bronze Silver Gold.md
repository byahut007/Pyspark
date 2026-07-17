LAB 7 — Batch ETL Pipeline Using Bronze → Silver → Gold
Objective:

By the end of this lab, learners will:

✔ Implement a batch ingestion pipeline

✔ Use Delta Lake for incremental updates

✔ Apply ETL cleaning, standardization & enrichment

✔ Build Gold aggregates for analytics

✔ Implement ETL orchestration using Databricks Workflows


PART A — Setup the Project

Step 1 — Create a New Notebook
Go to Workspace → Your Folder → Create → Notebook
Name it: Lab7_Batch_ETL_Pipeline
Choose Python
Attach to your cluster

Step 2 — Create ETL Directory Structure
Run:

dbutils.fs.mkdirs("/mnt/lab7/bronze")
dbutils.fs.mkdirs("/mnt/lab7/silver")
dbutils.fs.mkdirs("/mnt/lab7/gold")


Verify:

dbutils.fs.ls("/mnt/lab7")

PART B — Batch Ingestion Into Bronze


Step 3 — Download Raw Source Data
Download a retail dataset:
source = "https://raw.githubusercontent.com/databricks/Spark-The-Definitive-Guide/master/data/retail-data/all/*.csv"

df_raw = spark.read.option("header", True).option("inferSchema", True).csv(source)


Preview data:

display(df_raw)

Step 4 — Write into Bronze


Store raw data in Delta:

df_raw.write.format("delta").mode("overwrite").save("/mnt/lab7/bronze/retail")


Register bronze table:

CREATE TABLE IF NOT EXISTS lab7_bronze_retail
USING delta
LOCATION '/mnt/lab7/bronze/retail';
Validate:

SELECT COUNT(*) FROM lab7_bronze_retail;


PART C — Apply Cleaning Logic Into Silver

Step 5 — Load Bronze Data


Load:

bronze_df = spark.read.format("delta").load("/mnt/lab7/bronze/retail")


Drop nulls:

df_clean = bronze_df.dropna()


Remove negative quantities:

from pyspark.sql.functions import col
df_clean = df_clean.filter(col("Quantity") > 0)


Normalize column names:

df_clean = df_clean.withColumnRenamed("InvoiceNo","invoice_no")\
                   .withColumnRenamed("StockCode","stock_code")

Step 6 — Write Into Silver


Write:

df_clean.write.format("delta").mode("overwrite").save("/mnt/lab7/silver/retail_clean")


Register table:

CREATE TABLE IF NOT EXISTS lab7_silver_retail
USING delta
LOCATION '/mnt/lab7/silver/retail_clean';


Preview:

SELECT * FROM lab7_silver_retail LIMIT 10;

PART D — Build a Gold Analytical Table

Step 7 — Create Revenue Table


Create:

from pyspark.sql.functions import sum, col, to_date

df_gold = df_clean.withColumn("date", to_date("InvoiceDate"))\
                  .groupBy("date")\
                  .agg(sum(col("UnitPrice") * col("Quantity")).alias("daily_revenue"))


Save Gold:

df_gold.write.format("delta").mode("overwrite").save("/mnt/lab7/gold/daily_revenue")


Register:

CREATE TABLE IF NOT EXISTS lab7_gold_daily_revenue
USING delta
LOCATION '/mnt/lab7/gold/daily_revenue';


PART E — Incremental ETL (Simulate Incremental File Arrival)

Step 8 — Create Sample Incremental File


Create:

data_incremental = [(12345, "85123A", "White Mug", 10, 2.5, "2023-01-05", "United Kingdom")]
columns = ["invoice_no","stock_code","description","Quantity","UnitPrice","InvoiceDate","Country"]

df_inc = spark.createDataFrame(data_incremental, columns)


Save incremental CSV for simulation:

df_inc.write.mode("overwrite").option("header", True).csv("/mnt/lab7/new_data")


PART F — Re-Execute Batch ETL with Merge Logic

Step 9 — Read Incremental File


Load:

df_new = spark.read.option("header",True).csv("/mnt/lab7/new_data")


Add schema alignment:

from pyspark.sql.functions import to_date
df_new = df_new.withColumn("InvoiceDate", to_date("InvoiceDate"))

Step 10 — Merge Into Silver


Run MERGE to update table:

MERGE INTO lab7_silver_retail AS tgt
USING df_new AS src
ON tgt.invoice_no = src.invoice_no
WHEN MATCHED THEN UPDATE SET Quantity = src.Quantity, UnitPrice = src.UnitPrice
WHEN NOT MATCHED THEN INSERT *;
Validate:

SELECT * FROM lab7_silver_retail WHERE invoice_no = 12345;
