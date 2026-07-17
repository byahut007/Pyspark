from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from typing import Tuple
from pyspark.sql import functions as F

def define_movie_schema()-> StructType:
    schema= StructType([
        StructField("movie_id",IntegerType(), True),
        StructField("title",StringType(), True),
        StructField("genre",StringType(), True),
        StructField("release_date",StringType(), True),
        StructField("revenue_million",DoubleType(), True)
    ])
    return schema

def load_movies_data(spark:SparkSession,path:str, schema: StructType)-> DataFrame:
    df=spark.read.csv(path, header=True, inferSchema=True)
    df=df.withColumn("release_date", F.to_date("release_date"))
    return df

def filter_by_date_range(df:DataFrame, start:str, end:str)-> DataFrame:
    return df.filter(F.col("release_date").between(start,end))

def total_revenue_by_genre(df:DataFrame)-> DataFrame:
    return df.groupBy("genre").agg(F.sum("revenue_million").alias("total_revenue"))

def compute_days_since_release(df:DataFrame)-> DataFrame:
    return df.withColumn("days_since_release", F.date_diff(F.current_date(), F.to_date(F.col("release_date"))))

def get_highest_grossing_movie(df:DataFrame)-> Tuple[str, float]:
    res=df.orderBy(F.col("revenue_million").desc()).first()
    return res["title"],res["revenue_million"]