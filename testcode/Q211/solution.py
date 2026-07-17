from pyspark.sql import SparkSession, DataFrame
from typing import Tuple
from pyspark.sql import functions as F

def load_circulation_data(spark: SparkSession, path: str)-> DataFrame:
    df = spark.read.csv(path, header=True, inferSchema=True)
    df = df.withColumn("borrow_date", F.to_date(F.col("borrow_date")))
    df = df.withColumn("return_date", F.to_date(F.col("return_date")))
    return df

def with_late_days(df: DataFrame)-> DataFrame:
    return df.withColumn("days", F.date_diff(F.col("return_date"), F.col("borrow_date")))

def filter_valid_loans(df: DataFrame)-> DataFrame:
    return df.filter(F.col("days")>=0)

def category_popularity(df: DataFrame)-> DataFrame:
    return df.groupBy("category").count().alias("borrows").withColumnRenamed("count", "borrows")

def top_category(df: DataFrame)-> Tuple[str,int]:
    return tuple(df.orderBy(F.col("borrows").desc(),F.col("category")).first())