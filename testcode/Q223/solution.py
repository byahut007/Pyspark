from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

def load_species_data(spark:SparkSession, path:str)-> DataFrame:
    df =spark.read.csv(path, header=True, inferSchema=True)
    df.withColumn("Last_Surveyed", F.to_date(F.col("Last_Surveyed")))
    return df

def rank_habitats_by_population(df:DataFrame)-> DataFrame:
    return df.groupBy("Habitat_Type").agg(F.sum("Population_Estimate").alias("total_population")).orderBy(F.col("total_population").desc()).limit(1)

def filter_critically_endangered(df:DataFrame)-> DataFrame:
    list1=["Endangered", "Critically Endangered"]
    return df.filter(F.col("Protection_Status").isin(list1))

def filter_recently_surveyed_endangered(df:DataFrame)-> DataFrame:
    return df.filter(F.col("protection_status")=="Endangered").orderBy(F.col("Last_Surveyed").desc()).limit(1)