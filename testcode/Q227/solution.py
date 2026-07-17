from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField,StringType, FloatType, DateType
from typing import Tuple
from pyspark.sql import functions as F

def define_medicine_schema()->StructType:
    schema= StructType([
        StructField("purchase_id",StringType(),True),
        StructField("medicine_name",StringType(),True),
        StructField("category",StringType(),True),
        StructField("purchase_date",DateType(),True),
        StructField("purchase_amount",FloatType(),True)
    ])
    return schema

def load_purchase_data(spark:SparkSession, path:str, schema:StructType)-> DataFrame:
    df=spark.read.schema(schema).csv(path, header=True, inferSchema=True)
    return df.withColumn("purchase_date",F.to_date("purchase_date"))


def filter_by_purchase_date_range(df:DataFrame, start:str, end:str)-> DataFrame:
    return df.filter(F.col("purchase_date").between(start,end))

def total_purchase_by_category(df:DataFrame)-> DataFrame:
    return df.groupBy("category").agg(F.sum("purchase_amount").alias("total_purchase"))

def compute_days_since_purchase(df:DataFrame)-> DataFrame:
    return df.withColumn("days_since_purchase", F.datediff(F.current_date(), F.col("purchase_date")))

def get_top_medicine_by_sales(df:DataFrame)-> Tuple[str, float]:
    res= df.orderBy(F.col("purchase_amount").desc()).first()
    return res["medicine_name"],res["purchase_amount"]