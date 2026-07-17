from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

def load_irrigation_data(spark:SparkSession,path:str)-> DataFrame:
    df=spark.read.csv(path, header=True, inferSchema=True)
    df.withColumn("irrigation_date",F.to_date("irrigation_date"))
    df.printSchema()
    return df


def with_month(df:DataFrame)-> DataFrame:
    df=df.withColumn("month", F.to_date(F.date_trunc("month", F.col("irrigation_date"))))
    return df

def filter_valid(df:DataFrame)-> DataFrame:
    return df.filter(F.col("liters_used")>=0)

def monthly_crop_water(df:DataFrame)-> DataFrame:
    return df.groupBy("crop_type","month").agg(F.sum("liters_used").alias("total_liters"))

def top_crop_by_month(df:DataFrame)-> str:
    res= df.groupBy("crop_type").agg(F.sum("total_liters").alias("total_liters")).orderBy(F.col("total_liters").desc()).first()
    return res["crop_type"]
