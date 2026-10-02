import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, current_date

# 1. Initialize Glue and Spark Contexts
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 2. Define S3 Paths (Replace 'XXXX' with your actual bucket suffix!)
# We use s3a:// which is the standard Hadoop S3 filesystem protocol
BUCKET_NAME = "skyhigh-airlines-lake-b844ab7b" 
bronze_path = f"s3a://{BUCKET_NAME}/bronze/raw_flight_data.csv"
silver_path = f"s3a://{BUCKET_NAME}/silver/flight_data/"

# 3. Read the Raw Data from Bronze
print(f"Reading data from {bronze_path}...")
df_bronze = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(bronze_path)

# 4. Clean and Transform the Data (Silver Layer Logic)
print("Cleaning and transforming data...")
df_silver = df_bronze.dropna() \
    .withColumn("processing_date", current_date()) \
    .withColumn("airline", col("airline").cast("string")) # Ensure partition column is string

# 5. Write to Silver Layer as Partitioned Parquet
print(f"Writing partitioned Parquet data to {silver_path}...")
# partitionBy creates folders like: silver/flight_data/airline=SkyHigh/
df_silver.write \
    .format("parquet") \
    .mode("overwrite") \
    .partitionBy("airline") \
    .save(silver_path)

print("✅ Glue ETL Job completed successfully!")

# 6. Commit the job (Required by AWS Glue to mark it as successful in the console)
job.commit()