   # Use the official Apache Airflow image as our base
   FROM apache/airflow:2.8.1-python3.9

   # Switch to the airflow user (required by Airflow's Docker image)
   USER airflow

   # Copy our requirements file into the container
   COPY requirements.txt /requirements.txt

   # Install the additional providers we need (AWS, Snowflake)
   RUN pip install --no-cache-dir -r /requirements.txt
