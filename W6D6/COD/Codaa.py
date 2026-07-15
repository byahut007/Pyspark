import os
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, trim, min, max, avg
from pyspark.sql.types import IntegerType

spark = SparkSession.builder \
    .appName("CustomerFeedbackInsights") \
    .getOrCreate()


csv_content = """email,rating,comment
alice@mail.com,5,Great service
,3,Okay but could be better
bob@mail.com,,No rating given
invalid_email,4,Good experience
eve@mail.com,4,Nice
david@mail.com,3,Average
"""

csv_path = "data_feedback.csv"
with open(csv_path, "w") as f:
    f.write(csv_content)

print(f"Sample dataset created at: {csv_path}\n")


def load_feedback_data(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.csv(path, header=True, inferSchema=True)

def clean_missing_and_invalid_emails(df: DataFrame) -> DataFrame:
    return df.filter(col("email").isNotNull() & (trim(col("email")) != ""))

def compute_rating_stats(df: DataFrame) -> dict:
    df_int = df.withColumn("rating", col("rating").cast(IntegerType()))
    
    df_filtered = df_int.filter(col("rating").isNotNull())
    
    stats = df_filtered.agg(
        min("rating").alias("min_rating"),
        max("rating").alias("max_rating"),
        avg("rating").alias("avg_rating")
    ).collect()[0]

    return {
        "min_rating": stats["min_rating"],
        "max_rating": stats["max_rating"],
        "avg_rating": float(stats["avg_rating"]) if stats["avg_rating"] is not None else 0.0
    }

def count_ratings(df: DataFrame) -> int:
    return df.filter(col("rating").isNotNull()).count()

def most_common_rating(df: DataFrame) -> int:
    df_int = df.withColumn("rating", col("rating").cast(IntegerType()))
    
    df_valid = df_int.filter(col("rating").between(1, 5))
    
    counts = df_valid.groupBy("rating").count().orderBy(col("count").desc(), col("rating").asc())

    first_row = counts.first()
    if first_row is not None:
        return first_row["rating"]
    return 0


print("--- Testing load_feedback_data ---")
df = load_feedback_data(spark, csv_path)
df.show()

print("--- Testing clean_missing_and_invalid_emails ---")
cleaned_emails_df = clean_missing_and_invalid_emails(df)
cleaned_emails_df.show()

print("--- Testing compute_rating_stats ---")
stats = compute_rating_stats(df)
print(stats, "\n")

print("--- Testing count_ratings ---")
rating_count = count_ratings(df)
print(f"Total valid ratings: {rating_count}\n")

print("--- Testing most_common_rating ---")
common_rating = most_common_rating(df)
print(f"Most common rating: {common_rating}\n")