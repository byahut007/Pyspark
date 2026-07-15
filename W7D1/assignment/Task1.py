"""
Function 1:
Create & return SparkSession
Function 2: Create dataframe
Use inferschema for quick creation
Output Dataframe
Function 3: top 3 cars by price
Output shall be dataframe
Function 4: top 2 popular
Output shall be a list
Function 5: Latest car model
Output should be a string

"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

def createSession()->SparkSession:
    spark = SparkSession.builder.appName("Cars Data Analysis").getOrCreate()
    return spark

def createDataframe(spark:SparkSession,path:str)->DataFrame:
    df=spark.read.csv(path,header=True,inferSchema=True)
    return df

def topNCarsbyPrice(df:DataFrame,n:int)->DataFrame:
    return df.sort(F.col("Price").desc()).select("Brand","Price").limit(n)

def topNPopularTransmission(df:DataFrame,n:int)->list:
    return df.groupby("Transmission").count().orderBy(F.col("count").desc()).limit(n).rdd.flatMap(lambda x:x).collect()

def latestCarModel(df:DataFrame):
    df.orderBy("Year").select("Model").collect()[0][0]

spark = createSession()
df=createDataframe(spark,"automobile_cars.csv")
df.show()

res1=topNCarsbyPrice(df,3)
res1.show()

re2=topNPopularTransmission(df,2)
print(re2)