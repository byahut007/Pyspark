from pyspark.sql import SparkSession, DataFrame

from pyspark.sql import functions as F

def load_bookings_data(spark:SparkSession, path:str)->DataFrame:
    df = spark.read.csv(path, header=True, inferSchema=True)
    df.withColumn("show_date", F.to_date(F.col("show_date")))
    return df

def load_movie_info(spark:SparkSession, path:str)->DataFrame:
    df = spark.read.csv(path, header=True, inferSchema=True)
    return df

def filter_valid_bookings(df:DataFrame)->DataFrame:
    return df.filter((F.col("seats_booked")>=0) & (F.col("show_duration_min")>=0))

def with_overbooking_flag(df:DataFrame)->DataFrame:
    return df.withColumn("overbooked", F.when(F.col("seats_booked")>F.col("total_seats"),1).otherwise(0))

def join_movie_info(bookings:DataFrame ,info_df:DataFrame)->DataFrame:
    return bookings.join(info_df, on="movie_id", how="left")

def movie_occupancy_efficiency(df:DataFrame)->str:
    df = df.groupBy("movie_id", "total_seats").agg(
        F.sum("seats_booked").alias("total_booked")
    )

    df= df.withColumn("effeciency", F.when(F.col("total_seats")==0, 0.0).otherwise(F.col("total_booked")/F.col("total_seats")))
    return df.orderBy(F.col("effeciency").desc()).collect()[0]["movie_id"]
