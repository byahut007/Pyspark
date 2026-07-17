from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from typing import Tuple

def load_listens_data(spark:SparkSession,path:str)-> DataFrame:
    df=spark.read.csv(path, header=True,inferSchema=True)
    return df.withColumn("start_time", F.to_date("start_time"))

def filter_valid_sessions(df:DataFrame)-> DataFrame:
    return df.filter(F.col("episode_id").isNotNull())

def episode_minutes(df:DataFrame)-> DataFrame:
    return df.groupby("episode_id").agg(F.sum("duration_min").alias("total_min"))

def device_counts(df:DataFrame)-> DataFrame:
    return df.groupBy("device_type").agg(F.count("*").alias("sessions"))

def top_episode(df:DataFrame)-> Tuple[str, int]:
    return tuple(df.orderBy(F.col("total_min").desc()).first())