from pyspark.sql import SparkSession, DataFrame
from typing import Tuple
from pyspark.sql import functions as F

def load_university_data(spark:SparkSession, path1:str, path2:str)-> Tuple[DataFrame, DataFrame]:
    df1=spark.read.csv(path1, header=True, inferSchema=True)
    df2=spark.read.csv(path2, header=True, inferSchema=True)
    return (df1,df2)


def join_student_data(df1:DataFrame, df2: DataFrame)-> DataFrame:
    return df2.join(df1, on="user_id", how="inner")

def enrich_full_name(df:DataFrame)-> DataFrame:
    res= df.withColumn("full_name",F.coalesce(F.concat_ws(" ", F.col("first_name"), F.col("last_name"))))
    return res

def find_students(df:DataFrame)-> DataFrame:
    return df.filter(F.col("grade")=="F")