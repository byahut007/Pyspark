from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from typing import Tuple

def load_flight_data(spark:SparkSession, path:str)-> DataFrame:
    df=spark.read.csv(path, header=True,inferSchema=True)
    return df.withColumn("flight_date",F.to_date("flight_date"))

def filter_valid_flights(df:DataFrame)-> DataFrame:
    return df.filter((F.col("flight_id").isNotNull())&(F.col("scheduled_minutes")>0))

def add_delay_minutes(df:DataFrame)-> DataFrame:
    return df.withColumn("delay_minutes",F.col("actual_minutes")-F.col("scheduled_minutes"))

def filter_delayed_flights(df:DataFrame,threshold:int)-> DataFrame:
    return df.filter(F.col("delay_minutes")> threshold).select("flight_id","airline","delay_minutes")

def avg_delay_by_airline(df:DataFrame)-> DataFrame:
    return df.groupBy("airline").agg(F.avg("delay_minutes").alias("avg_delay"))

def busiest_route(df:DataFrame)-> Tuple[str,int]:
    res=df.groupBy("origin", "destination").count().orderBy(F.col("count").desc(),F.col("origin"), F.col("destination")).limit(1).rdd.flatMap(lambda x:x).collect()
    str1=res[0]+ "-" + res[1]
    return str(str1),int(res[2])