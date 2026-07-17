LAB 8 — Real-Time Streaming ETL Pipeline (Auto Loader + Delta Lake)
Objective:

Learners will:

✔ Build streaming ingestion using Auto Loader

✔ Use checkpoints for fault tolerance

✔ Write streaming Bronze, Silver, Gold layers

✔ Apply schema evolution

✔ Test end-to-end stream processing


PART A — Create Streaming Directory Structure


Step 1 — Create Notebook
Name: Lab8_Streaming_ETL_Pipeline
Attach cluster.
Step 2 — Prepare Directories


Run:

dbutils.fs.mkdirs("/mnt/lab8/raw_stream")
dbutils.fs.mkdirs("/mnt/lab8/bronze_stream")
dbutils.fs.mkdirs("/mnt/lab8/silver_stream")
dbutils.fs.mkdirs("/mnt/lab8/gold_stream")


Verify:

dbutils.fs.ls("/mnt/lab8")


PART B — Configure Auto Loader Stream

Step 3 — Start Streaming Reader


Run:

from pyspark.sql.functions import *

stream_df = (spark.readStream.format("cloudFiles")
             .option("cloudFiles.format","csv")
             .option("header","true")
             .option("inferSchema","true")
             .load("/mnt/lab8/raw_stream"))
Display streaming schema:

stream_df.printSchema()


PART C — Write to Bronze (Streaming)
Step 4 — Write Stream to Bronze


Run:

bronze_stream = (stream_df.writeStream.format("delta")
                .option("checkpointLocation","/mnt/lab8/chk/bronze")
                .outputMode("append")
                .start("/mnt/lab8/bronze_stream"))
Keep this streaming job running.



PART D — Simulate Incoming Streaming Files
Step 5 — Write Small Batches


Create small CSV files:

df_small = spark.createDataFrame(
    [(1,"A",10,2.5,"2023-01-01","UK"),
     (2,"B",20,3.0,"2023-01-01","UK")],
    ["invoice_no","stock_code","Quantity","UnitPrice","InvoiceDate","Country"]
)
df_small.write.option("header","true").csv("/mnt/lab8/raw_stream")
Bronze stream will automatically ingest them.


Step 6 — Check Bronze Table


Query:

spark.read.format("delta").load("/mnt/lab8/bronze_stream").show()


PART D — Simulate Incoming Streaming Files

Step 5 — Write Small Batches


Create small CSV files:

df_small = spark.createDataFrame(
    [(1,"A",10,2.5,"2023-01-01","UK"),
     (2,"B",20,3.0,"2023-01-01","UK")],
    ["invoice_no","stock_code","Quantity","UnitPrice","InvoiceDate","Country"]
)
df_small.write.option("header","true").csv("/mnt/lab8/raw_stream")


Bronze stream will automatically ingest them.


Step 6 — Check Bronze Table


Query:

spark.read.format("delta").load("/mnt/lab8/bronze_stream").show()


PART F — Build Gold Table in Streaming

Step 9 — Create Gold Revenue Streaming Table


Aggregate stream:

gold_df = silver_df.groupBy("InvoiceDate").agg(sum(col("Quantity") * col("UnitPrice")).alias("daily_revenue"))


Write:

gold_stream = (gold_df.writeStream.format("delta")
                .option("checkpointLocation","/mnt/lab8/chk/gold")
                .outputMode("complete")
                .start("/mnt/lab8/gold_stream"))

Step 10 — Validate Gold


Run:

spark.read.format("delta").load("/mnt/lab8/gold_stream").show()


Lab 8 Completion Criteria


✔ Auto Loader configured

✔ Bronze, Silver, Gold streaming tables created

✔ Incremental streaming files processed

✔ Gold layer aggregates created in real-time

✔ Checkpoints ensure fault tolerance