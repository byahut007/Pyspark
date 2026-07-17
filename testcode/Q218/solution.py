from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField,IntegerType, StringType, DateType, DoubleType
from pyspark.sql import functions as F
from typing import List

def define_visit_schema()-> StructType:
    schema= StructType([
        StructField("visit_id",IntegerType(),True),
        StructField("patient_id",IntegerType(),True),
        StructField("department",StringType(),True),
        StructField("visit_date",DateType(),True),
        StructField("billing_amount",DoubleType(),True),
        StructField("status",StringType(),True)
    ])

    return schema

def load_patient_visits(spark:SparkSession, path:str, schema:StringType)-> DataFrame:
    return spark.read.csv(path,header=True,inferSchema=True,schema=schema)

def top_n_departments_by_billing(df:DataFrame, n:int)-> DataFrame:
    return df.groupBy("department").agg(F.sum("billing_amount").alias("total_billing")).orderBy(F.col("total_billing").desc()).limit(n)

def list_active_departments(df:DataFrame)-> List[str]:
    return df.filter(F.col("status")=="active").select("department").distinct().orderBy("department").rdd.flatMap(lambda x:x).collect()