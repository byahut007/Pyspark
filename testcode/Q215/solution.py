from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import  StructType, StructField, StringType, IntegerType, FloatType, DateType
import datetime as dt
from typing import List



def create_vehicle_schema_and_load(spark:SparkSession)-> DataFrame:
    data = [
        ("Hyundai", "i20", dt.date(2020, 6, 15), 1200, 18.5, "active"),
        ("Hyundai", "Creta", dt.date(2018, 3, 10), 1500, 16.0, "inactive"),
        ("Toyota", "Corolla", dt.date(2019, 1, 20), 1800, 15.5, "active"),
        ("Toyota", "Camry", dt.date(2017, 9, 5), 900, 14.0, "active"),
        ("Ford", "Figo", dt.date(2021, 11, 1), 700, 17.0, "active"),
        ("Ford", "EcoSport", dt.date(2016, 2, 12), 1100, 13.5, "inactive"),
    ]

    schema= StructType([
        StructField("maker", StringType(),True),
        StructField("model", StringType(),True),
        StructField("manufacture_date", DateType(),True),
        StructField("units_sold", IntegerType(),True),
        StructField("mileage", FloatType(),True),
        StructField("status", StringType(),True)
    ])

    return spark.createDataFrame(data, schema)

def filter_active_vehicles(df:DataFrame)-> DataFrame:
    return df.filter(F.col("status")=="active")

def top_n_brands_by_avg_mileage(df:DataFrame, n:int)-> DataFrame:
    res=df.groupBy(F.col("maker")).agg(F.avg("mileage").alias("average_mileage")).orderBy(F.col("average_mileage").desc()).limit(n)
    return res

def calculate_vehicle_age(df:DataFrame, reference_year:int)-> DataFrame:
    res= df.withColumn("vehicle_age", reference_year-F.year(F.col("manufacture_date")))
    return res
 
def top_highest_selling_models(df:DataFrame,n:int)-> DataFrame:
    res=df.groupBy(F.col("model")).agg(F.sum("units_sold").alias("units_sold")).orderBy(F.col("units_sold").desc()).limit(n)
    return res

def list_unique_car_makers(df:DataFrame)-> List[str]:
    res= sorted(df.select("maker").distinct().rdd.flatMap(lambda x:x).collect())
    return res