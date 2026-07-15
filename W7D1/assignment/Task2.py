from pyspark.sql import SparkSession
from pyspark.sql import functions as F

if __name__=="__main__":
    print("Application Started")

spark = SparkSession.builder.appName("ltm streaming").getOrCreate()
stream_df = spark.readStream.format("socket").option("host","127.0.0.1").option("port", "1111").load()


print(stream_df.isStreaming)

stream_df.printSchema()

# Split the lines into words
stream_words_df = stream_df.select(
   F.explode(
       F.split(stream_df.value, " ")
   ).alias("word")
)
stream_wordCount_df = stream_words_df.groupBy("word").count()
 # Start running the query that prints the running counts to the console
write_query = stream_wordCount_df.writeStream.outputMode("complete").format("console").start()
write_query.awaitTermination()

