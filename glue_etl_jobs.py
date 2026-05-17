import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, current_timestamp

# Start Spark
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# 1. Read from Bronze Layer
bronze_path = "s3://efe-data-engineering-bronze/"
df = spark.read.json(bronze_path)

# 2. Transform and clean data
# JSON data is a bit nested. We only take temperature, windspeed 
# and time from 'current_weather' and flatten it.
if "current_weather" in df.columns:
    df_cleaned = df.select(
        col("latitude"),
        col("longitude"),
        col("current_weather.temperature").alias("temperature"),
        col("current_weather.windspeed").alias("windspeed"),
        col("current_weather.time").alias("observation_time"),
        current_timestamp().alias("processed_at") # Add processing time
    )
else:
    df_cleaned = df

# 3. Write cleaned data as Parquet (Silver Layer)
silver_path = "s3://efe-data-engineering-silver/"

# Save as Parquet format. 
# We use append mode so it adds new data instead of overwriting.
df_cleaned.write.mode("append").parquet(silver_path)

print("ETL Success: Data saved to Silver layer as Parquet.")