from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, DateType, IntegerType, FloatType
import datetime

# if __name__ == "__main__":
#     spark = SparkSession.builder.appName("VehicleData").getOrCreate()
    
#     schema = StructType([
#         StructField("maker", StringType(), True),
#         StructField("model", StringType(), True),
#         StructField("manufacture_date", DateType(), True),
#         StructField("units_sold", IntegerType(), True),
#         StructField("mileage", FloatType(), True),
#         StructField("status", StringType(), True)
#     ])
    
#     data = [
#         ("Honda", "Civic", datetime.date(2020, 5, 10), 15000, 18.5, "active"),
#         ("Honda", "Accord", datetime.date(2018, 3, 15), 9000, 15.2, "inactive"),
#         ("Hyundai", "Elantra", datetime.date(2021, 8, 20), 12000, 17.5, "active"),
#         ("Hyundai", "Tucson", datetime.date(2019, 11, 5), 8500, 14.8, "active"),
#         ("Toyota", "Corolla", datetime.date(2022, 1, 12), 22000, 19.5, "active"),
#         ("Toyota", "Camry", datetime.date(2017, 6, 30), 6000, 16.0, "inactive")
#     ]
    
#     df = spark.createDataFrame(data, schema)
    
#     df_active = df.filter(F.col("status") == "active")
#     df_active.printSchema()
#     df_active.show()
    
#     df_top_mileage = (
#         df.groupBy("maker")
#         .agg(F.avg("mileage").alias("average_mileage"))
#         .orderBy(F.col("average_mileage").desc())
#         .limit(2)
#     )
#     df_top_mileage.show()
    
#     df_age = df.withColumn("vehicle_age", 2025 - F.year(F.col("manufacture_date")))
#     df_age.show()
    
#     df_top_selling = df.orderBy(F.col("units_sold").desc()).limit(2)
#     df_top_selling.show()
    
#     unique_makers = sorted(df.select("maker").distinct().rdd.flatMap(lambda x: x).collect())
#     print(unique_makers)

help(datetime)