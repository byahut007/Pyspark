from pyspark.sql import SparkSession, DataFrame

from pyspark.sql import functions as F


def load_rides_csv(spark:SparkSession, path:str)-> DataFrame:
    df= spark.read.csv(path, header=True, inferSchema=True)
    return df

def find_loyal_customers(df:DataFrame, n:int)-> DataFrame:
    res=df.groupBy("CustomerID").count().filter(F.col("count")>=n).select("CustomerID")
    return res

def apply_discounts(df: DataFrame, loyal_customers: DataFrame)-> DataFrame:
    df1 = loyal_customers.withColumn("is_loyal", F.lit(True))
    result =df.join(df1, on="CustomerID", how="left")

    result = result.withColumn("discount", F.when(F.col("is_loyal")==True, 0.10).otherwise(0.07))
    return result

def top_three_longest_trips(df:DataFrame)-> DataFrame:
    return df.select("RideId","source","destination", "distance").orderBy(F.col("distance").desc()).limit(3)

def get_top_earners(df:DataFrame)-> DataFrame:
    return df.groupBy("DriverID").agg(F.sum("earnings").alias("total_earnings")).limit(3)