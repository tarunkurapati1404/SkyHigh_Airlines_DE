# ✈️ SkyHigh Airlines: End-to-End Data Engineering Pipeline

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PySpark-3.4-orange?style=for-the-badge&logo=apache-spark&logoColor=white" />
  <img src="https://img.shields.io/badge/Databricks-Unity_Catalog-red?style=for-the-badge&logo=databricks&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS_S3-Data_Lake-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white" />
  <img src="https://img.shields.io/badge/Snowflake-Data_Warehouse-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache_Airflow-Orchestration-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Power_BI-Visualization-F2C811?style=for-the-badge&logo=power-bi&logoColor=black" />
</p>

---

## 📖 Project Overview

This project automates the ingestion, cleaning, transformation, and modeling of airline flight data to identify operational bottlenecks and delay metrics. By building a modern **Data Lakehouse** and **Star Schema**, this pipeline processes raw CSV data and delivers actionable business insights directly to an executive Power BI dashboard.

---

## 🏗️ Architecture Diagram

```text
[ Raw CSV Data ] 
        │
        ▼ (Python/Boto3 Ingestion)
[ AWS S3 - Bronze Layer ] 
        │
        ▼ (Databricks PySpark + Unity Catalog IAM Role)
[ AWS S3 - Silver Layer (Partitioned Parquet) ] 
        │
        ▼ (Databricks PySpark Aggregations)
[ AWS S3 - Gold Layer (Partitioned Parquet) ] 
        │
        ▼ (ELT: COPY INTO / Direct Load)
[ Snowflake Data Warehouse (Star Schema) ] 
        │
        ▼ (Native Connection)
[ 📊 Power BI Executive Dashboard ]

* Orchestrated by: Apache Airflow (Containerized via Docker)
```

---

## 🛠️ Tech Stack

| Category | Technology Used |
| :--- | :--- |
| **Cloud Storage** | AWS S3 (Data Lake) |
| **Compute & Processing** | Databricks (PySpark on Serverless) |
| **Data Governance** | Databricks Unity Catalog (IAM Role Integration) |
| **Data Warehousing** | Snowflake |
| **Orchestration** | Apache Airflow (Dockerized) |
| **Visualization** | Microsoft Power BI |
| **IaC & Version Control** | Terraform, Git, GitHub |

---

## 📂 Project Structure

```text
skyhigh-data-pipeline/
│
├── dags/                  # Apache Airflow DAG definitions
├── include/               # Helper scripts and assets
├── notebooks/             # Databricks PySpark notebooks (Silver/Gold layers)
├── terraform/             # Infrastructure as Code (AWS S3, IAM, etc.)
├── Dockerfile             # Custom Airflow container configuration
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🚀 How It Works

1. **Ingestion:** A Python script using `boto3` generates mock flight data and uploads it to the AWS S3 `bronze/` layer.
2. **Processing (Silver):** Databricks, securely authenticated via Unity Catalog and an AWS IAM Role (no hardcoded keys), reads the CSV, cleans it, and writes it as partitioned Parquet files to the `silver/` layer.
3. **Aggregation (Gold):** A second Databricks notebook applies business logic (e.g., calculating delay percentages) and writes aggregated metrics to the `gold/` layer.
4. **Modeling (ELT):** Data is loaded into Snowflake and transformed using SQL into a highly optimized Star Schema (`DIM_AIRLINE`, `DIM_AIRPORT`, `FACT_DAILY_FLIGHT_PERFORMANCE`).
5. **Visualization:** Power BI connects directly to the Snowflake Star Schema in Import Mode for sub-second dashboard performance.
6. **Orchestration:** The entire workflow is defined as a Directed Acyclic Graph (DAG) in Apache Airflow and containerized using Docker for environmental reproducibility.

---

## 🐛 Challenges & Solutions (Real-World Troubleshooting)

| Challenge Encountered | Root Cause | Solution Implemented |
| :--- | :--- | :--- |
| **Cloud Provider Service Restrictions** | Encountered account-level `AccessDeniedException` when attempting to provision AWS Glue ETL jobs via Terraform and CLI. | Pivoted to a more modern architecture: Replaced Glue entirely with Databricks. Implemented Databricks Unity Catalog with an External Location and AWS IAM Role trust policy, eliminating hardcoded credentials for a secure, enterprise-grade setup. |
| **Athena Query Cost Optimization** | Querying unpartitioned data scans entire datasets, increasing compute costs. | Partitioned the Silver and Gold Parquet layers by airline, allowing query engines like Athena to use Partition Pruning and scan only relevant S3 folders. |
| **Docker Environment Consistency** | Local Python environments often conflicted with production cloud environments. | Containerized the Airflow orchestration layer using a custom `Dockerfile` and `requirements.txt`, ensuring 100% reproducibility across environments. |

---

## 🚀 Future Enhancements

* Implement `dbt` within Snowflake for more modular, version-controlled SQL transformations.
* Add Great Expectations or Soda Core data quality tests between the Bronze and Silver layers.
* Set up GitHub Actions for CI/CD to automatically run `terraform plan` and `docker build` on pull requests.