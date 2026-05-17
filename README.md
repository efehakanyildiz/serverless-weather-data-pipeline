# Serverless Weather Data Pipeline (Medallion Architecture) 🌦️

## 📌 Project Overview
This project is an end-to-end, fully serverless data engineering pipeline built on AWS. It extracts real-time weather data for a specific location (RAMS Park, Istanbul) via an external API, processes it using PySpark, and makes it available for SQL-based analytics using the Medallion Architecture (Bronze, Silver, Gold layers).

## 🏗️ Architecture & Workflow
1. **Ingestion (Event-Driven):** `Amazon EventBridge` triggers an `AWS Lambda` function every hour.
2. **Bronze Layer (Raw Data):** The Lambda function fetches data from the Open-Meteo API and stores the raw JSON files into an `Amazon S3` bucket (Bronze).
3. **ETL Process (Data Processing):** `AWS Glue` (PySpark) job reads the raw JSON files, flattens the schema, casts data types, and converts the data into an optimized `Parquet` format.
4. **Silver/Gold Layer (Cleaned & Analytics):** The processed Parquet files are stored in a separate S3 bucket (Silver).
5. **Analytics (Querying):** `Amazon Athena` is used to query the processed data using standard SQL for reporting and insights.

## 🛠️ Technologies Used
* **Compute:** AWS Lambda (Python)
* **Storage:** Amazon S3
* **ETL & Data Processing:** AWS Glue (PySpark)
* **Analytics:** Amazon Athena
* **Orchestration:** Amazon EventBridge

## 🚀 Key Achievements
* Handled the **"Small File Problem"** by batch-processing hourly JSON files into highly compressed Parquet files using Spark.
* Designed a completely **Serverless** architecture, resulting in nearly $0 monthly cloud costs (utilizing AWS Free Tier).
* Structured the data lake following the industry-standard **Medallion Architecture**.

## 📊 Sample Query (Athena)
```sql
SELECT 
    observation_time, 
    temperature, 
    wind_speed 
FROM weather_data 
ORDER BY observation_time DESC;
