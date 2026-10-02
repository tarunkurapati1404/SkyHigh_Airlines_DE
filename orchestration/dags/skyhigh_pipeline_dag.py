from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# 1. Default arguments for all tasks in this DAG
default_args = {
    'owner': 'tarun',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 2. Define the DAG
with DAG(
    dag_id='skyhigh_airlines_end_to_end_pipeline',
    default_args=default_args,
    description='Automates the SkyHigh Airlines Bronze -> Silver -> Gold -> Snowflake pipeline',
    schedule_interval='@daily', # Runs every day at midnight
    start_date=datetime(2026, 1, 1),
    catchup=False, # Do not run for past dates
    tags=['skyhigh', 'airlines', 'data_engineering'],
) as dag:

    # TASK 1: Ingest Data
    # PRODUCTION NOTE: In a real job, this would be a PythonOperator calling our ingest_flight_data.py script,
    # or an S3 Sensor waiting for a new file to land.
    ingest_data = BashOperator(
        task_id='ingest_raw_flight_data_to_s3_bronze',
        bash_command='echo "✅ Running Python script to ingest raw CSV into S3 Bronze layer..."'
    )

    # TASK 2: Transform to Silver (Databricks)
    # PRODUCTION NOTE: In a real job, this would be the DatabricksSubmitRunOperator 
    # triggering our Databricks Notebook via the Databricks REST API.
    transform_silver = BashOperator(
        task_id='transform_bronze_to_silver_databricks',
        bash_command='echo "✅ Triggering Databricks Unity Catalog job to clean data and write partitioned Parquet to S3 Silver..."'
    )

    # TASK 3: Transform to Gold (Databricks)
    transform_gold = BashOperator(
        task_id='transform_silver_to_gold_databricks',
        bash_command='echo "✅ Triggering Databricks job to aggregate metrics and write to S3 Gold layer..."'
    )

    # TASK 4: Load to Snowflake
    # PRODUCTION NOTE: In a real job, this would be the SnowflakeOperator executing a COPY INTO command 
    # to load the Gold Parquet data from S3 into Snowflake.
    load_snowflake = BashOperator(
        task_id='load_gold_data_to_snowflake_dw',
        bash_command='echo "✅ Loading Gold Parquet data from S3 into Snowflake Star Schema (Fact & Dimension tables)..."'
    )

    # 3. Define the Execution Order (The "Directed Acyclic Graph")
    # The >> operator means "must finish successfully before the next task starts"
    ingest_data >> transform_silver >> transform_gold >> load_snowflake