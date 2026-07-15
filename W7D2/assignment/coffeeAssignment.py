from pyspark.sql import SparkSession, DataFrame

from pyspark.sql import functions as F


class CoffeeShopAnalyzer:
    def __init__(self):
        pass
    
    def create_sales_df(self, spark: SparkSession) -> DataFrame:
        sales_data = [
            (1, "S1", "Latte", 2, 200.0, "2025-01-01"),
            (2, "S2", "Espresso", 1, 120.0, "2025-01-01"),
            (3, "S1", "Cappuccino", 3, 300.0, "2025-01-02"),
            (4, "S3", "Latte", 1, 100.0, "2025-01-02"),
            (5, "S2", "Latte", 2, 200.0, "2025-01-03"),
            (6, "S3", "Mocha", 1, 150.0, "2025-01-03"),
            (7, "S1", "Espresso", 2, 240.0, "2025-01-04"),
            (8, "S2", "Cappuccino", 1, 120.0, "2025-01-04"),
            (9, "S3", "Latte", 2, 200.0, "2025-01-05"),
            (10, "S1", "Mocha", 1, 150.0, "2025-01-05"),
            (11, "S2", "Latte", 3, 300.0, "2025-01-06"),
            (12, "S3", "Espresso", 2, 240.0, "2025-01-06"),
            (13, "S1", "Latte", 1, 100.0, "2025-01-07"),
            (14, "S2", "Mocha", 2, 300.0, "2025-01-07"),
            (15, "S3", "Cappuccino", 1, 120.0, "2025-01-08")
            ]
        sales_data_column=["order_id","store_id","drink_type","quantity","revenue","order_date"]
        return spark.createDataFrame(sales_data, sales_data_column)
    
    def create_store_df(self, spark: SparkSession) -> DataFrame:
        store_data = [
            ("S1", "Mumbai", "West"),
            ("S2", "Delhi", "North"),
            ("S3", "Bangalore", "South"),
            ("S4", "Chennai", "South"),
            ("S5", "Pune", "West"),
            ("S6", "Kolkata", "East"),
            ("S7", "Hyderabad", "South"),
            ("S8", "Ahmedabad", "West"),
            ("S9", "Jaipur", "North"),
            ("S10", "Lucknow", "North"),
            ("S11", "Nagpur", "West"),
            ("S12", "Indore", "Central"),
            ("S13", "Surat", "West"),
            ("S14", "Bhopal", "Central"),
            ("S15", "Patna", "East")
            ]
        store_data_column=["store_id","city","region"]
        return spark.createDataFrame(store_data, store_data_column)
    
    def convert_order_date(self, df: DataFrame) -> DataFrame:
        return df.withColumn("order_date", F.to_date(F.col("order_date")))
    
    def filter_valid_sales(self, df: DataFrame) -> DataFrame:
        return df.filter((F.col("quantity")>0)&(F.col("revenue")>0))
    
    def filter_sales_by_date(self, df: DataFrame, start: str, end: str) -> DataFrame:
        return df.filter(F.col("order_date").between(start,end))
    
    def total_revenue_by_drink(self, df: DataFrame) -> DataFrame:
        return df.groupBy("drink_type").agg(F.sum("revenue").alias("total_revenue"))
    
    def total_quantity_per_store(self, df: DataFrame) -> DataFrame:
        return df.groupBy("store_id").agg(F.sum("quantity").alias("total_quantity"))
    
    def join_sales_store(self, sales_df: DataFrame, store_df: DataFrame) -> DataFrame:
        return sales_df.join(store_df, on="store_id", how="inner")
    
    def avg_revenue_per_drink(self, df: DataFrame) -> DataFrame:
        return df.groupBy("drink_type").agg(F.avg("revenue").alias("avg_revenue"))
    
    def top_drinks_by_revenue(self, df: DataFrame, n: int) -> DataFrame:
        return df.groupBy("drink_type").agg(F.sum("revenue").alias("sum_revenue")).sort(F.col("sum_revenue").desc()).limit(n)
    
    def get_unique_drinks(self, df: DataFrame) -> list:
        res= df.select("drink_type").distinct().rdd.flatMap(lambda x:x).collect()
        res.sort()
        return res
    
    def get_highest_revenue_drink(self, df: DataFrame) -> tuple:
        row = df.groupBy("drink_type").agg(F.sum("revenue").alias("total")).orderBy(F.col("total").desc()).first()
        return (row["drink_type"], row["total"])

    def add_revenue_category(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
            "revenue_category",
            F.when(F.col("revenue") >= 250, "High")
            .when(F.col("revenue").between(150, 249), "Medium")
            .otherwise("Low")
        )

    def compute_days_since_order(self, df: DataFrame) -> DataFrame:
        return df.withColumn("days_since_order", F.datediff(F.current_date(), F.col("order_date")))

    def revenue_percentage_by_drink(self, df: DataFrame) -> DataFrame:
        total_rev = df.agg(F.sum("revenue")).collect()[0][0]
        return df.groupBy("drink_type").agg(F.sum("revenue").alias("total_revenue")).withColumn(
            "percentage", F.round((F.col("total_revenue") / total_rev) * 100, 1)
        )

    def top_store_by_revenue(self, df: DataFrame) -> tuple:
        row = df.groupBy("store_id").agg(F.sum("revenue").alias("total")).orderBy(F.col("total").desc()).first()
        return (row["store_id"], row["total"])

    def filter_high_revenue_orders(self, df: DataFrame, threshold: float) -> DataFrame:
        return df.filter(F.col("revenue") > threshold)

    def orders_per_region(self, df: DataFrame, store_df: DataFrame) -> DataFrame:
        return df.join(store_df, on="store_id", how="inner").groupBy("region").agg(F.count("*").alias("total_orders"))

spark=SparkSession.builder.getOrCreate()


a=CoffeeShopAnalyzer()


sales_df=a.create_sales_df(spark)
# sales_df.show()

store_df=a.create_store_df(spark)


# store_df.show()

sales_df=a.convert_order_date(sales_df)
# sales_df.show()

res1=a.filter_valid_sales(sales_df)
# res1.show()

res2=a.filter_sales_by_date(sales_df,"2025-01-01","2025-01-05")
# res2.show()

res3=a.total_revenue_by_drink(sales_df)
# res3.show()

res4=a.total_quantity_per_store(sales_df)
# res4.show()

res5=a.join_sales_store(sales_df,store_df)
# res5.show()

res6=a.avg_revenue_per_drink(sales_df)
# res6.show()

res7=a.top_drinks_by_revenue(sales_df,2)
# res7.show()

res8=a.get_unique_drinks(sales_df)
# print(res8)

a.revenue_percentage_by_drink(sales_df)