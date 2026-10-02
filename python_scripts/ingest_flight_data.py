import boto3
import csv
import random
import logging
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

# 1. Setup Logging (Crucial for debugging in production)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 2. Configuration
# REPLACE THIS with the exact bucket name Terraform outputted in Day 1!
S3_BUCKET_NAME = "skyhigh-airlines-lake-b844ab7b" 
S3_BRONZE_PREFIX = "bronze/"
LOCAL_FILE_NAME = "raw_flight_data.csv"

def generate_mock_flight_data(num_records=100):
    """Generates realistic mock flight data and saves it locally."""
    logging.info(f"Generating {num_records} mock flight records...")
    
    airlines = ['SkyHigh', 'JetStream', 'AeroVista', 'CloudNine']
    origins = ['JFK', 'LAX', 'ORD', 'ATL', 'DFW']
    destinations = ['LHR', 'CDG', 'NRT', 'DXB', 'SIN']
    
    with open(LOCAL_FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write Header
        writer.writerow(['flight_id', 'airline', 'origin', 'destination', 'departure_time', 'arrival_time', 'passenger_count', 'status'])
        
        # Write Rows
        for i in range(num_records):
            flight_id = f"SH{i+1000}"
            airline = random.choice(airlines)
            origin = random.choice(origins)
            dest = random.choice(destinations)
            
            # Generate random times
            base_time = datetime.now() - timedelta(days=random.randint(1, 30))
            dep_time = base_time.strftime('%Y-%m-%d %H:%M:%S')
            arr_time = (base_time + timedelta(hours=random.randint(2, 14))).strftime('%Y-%m-%d %H:%M:%S')
            
            passengers = random.randint(50, 300)
            status = random.choice(['On Time', 'Delayed', 'Cancelled'])
            
            writer.writerow([flight_id, airline, origin, dest, dep_time, arr_time, passengers, status])
            
    logging.info(f"Successfully saved data to {LOCAL_FILE_NAME}")

def upload_to_s3(file_path, bucket_name, s3_key):
    """Uploads a file to the S3 Bronze layer using Boto3."""
    s3_client = boto3.client('s3')
    
    try:
        logging.info(f"Uploading {file_path} to s3://{bucket_name}/{s3_key}...")
        # upload_file is the standard method for uploading local files to S3
        s3_client.upload_file(file_path, bucket_name, s3_key)
        logging.info("✅ Upload successful!")
    except ClientError as e:
        logging.error(f"❌ Upload failed: {e}")
        raise

if __name__ == "__main__":
    # Step 1: Generate the data locally
    generate_mock_flight_data(num_records=1000)
    
    # Step 2: Define the S3 path (e.g., bronze/raw_flight_data.csv)
    s3_object_key = f"{S3_BRONZE_PREFIX}{LOCAL_FILE_NAME}"
    
    # Step 3: Upload to AWS S3
    upload_to_s3(LOCAL_FILE_NAME, S3_BUCKET_NAME, s3_object_key)