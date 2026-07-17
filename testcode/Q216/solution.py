from pyspark.sql import SparkSession, DataFrame

from pyspark.sql import functions as F


def load_inline_data(spark:SparkSession)-> DataFrame:
  data = [
        ("O1001", "PartnerA", "2025-12-01 10:00:00", "2025-12-01 12:00:00", "Traffic"),
        ("O1002", "PartnerA", "2025-12-01 09:00:00", "2025-12-01 10:30:00", "Traffic"),
        ("O1003", "PartnerB", "2025-12-02 14:00:00", "2025-12-02 18:00:00", "Weather"),
        ("O1004", "PartnerB", "2025-12-02 08:00:00", "2025-12-02 07:00:00", "Restaurant"),
        ("O1005", "PartnerC", "2025-12-03 11:00:00", "2025-12-03 13:00:00", "Restaurant"),
        ("O1006", "PartnerC", "2025-12-03 16:00:00", "2025-12-03 20:00:00", "Traffic"),
    ]
  
  column=["order_id","partner","expected_delivery","actual_delivery", "delay_reason"]

  df = spark.createDataFrame(data, column)
  return df
    
def compute_delay(df:DataFrame)-> DataFrame:
  calc=((F.unix_timestamp(F.col("actual_delivery"))-F.unix_timestamp(F.col("expected_delivery")))/3600.0)
  res= df.withColumn("delay_hours", F.when(calc >=0, calc).otherwise(0.0))
  return res    

def get_delayed_orders(df:DataFrame,threshold: float)-> DataFrame:
  df=df.withColumn("delay", (F.unix_timestamp(F.col("actual_delivery"))-F.unix_timestamp(F.col("expected_delivery")))/3600.0)
  return df.filter(F.col("delay")>threshold)
    
def most_delayed_partner(df:DataFrame)-> DataFrame:
  return df.groupBy("partner").agg(F.sum("delay_hours").alias("total_delay")).orderBy(F.col("total_delay").desc()).limit(1)
  
def most_common_delay_reason(df:DataFrame)-> DataFrame:
  return df.groupBy("delay_reason").agg(F.avg("delay_hours").alias("avg_delay")).orderBy(F.col("avg_delay").desc()).limit(1)