# 1. Terraform Settings: Define the required provider and version
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # Uses the latest stable 5.x version of the AWS provider
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

# 2. Provider Configuration: Tell Terraform which AWS region to use
provider "aws" {
  region = "eu-north-1"
}

# 3. Random ID: Generate a random string to ensure our S3 bucket name is globally unique
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# 4. S3 Bucket: Create the main Data Lake bucket
resource "aws_s3_bucket" "skyhigh_lake" {
  bucket = "skyhigh-airlines-lake-${random_id.bucket_suffix.hex}"
  
  tags = {
    Name        = "SkyHigh Airlines Data Lake"
    Environment = "Development"
    Owner       = "Tarun"
  }
}

# 5. S3 Bucket Versioning: Enable versioning (Best Practice for Data Lakes)
resource "aws_s3_bucket_versioning" "skyhigh_lake_versioning" {
  bucket = aws_s3_bucket.skyhigh_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

# 6. S3 Folders (Objects): Create the Medallion Architecture folders
# In S3, folders are technically just empty objects with a "/" at the end of their name.
resource "aws_s3_object" "bronze_folder" {
  bucket  = aws_s3_bucket.skyhigh_lake.id
  key     = "bronze/"
  content = ""
}

resource "aws_s3_object" "silver_folder" {
  bucket  = aws_s3_bucket.skyhigh_lake.id
  key     = "silver/"
  content = ""
}

resource "aws_s3_object" "gold_folder" {
  bucket  = aws_s3_bucket.skyhigh_lake.id
  key     = "gold/"
  content = ""
}

# 7. IAM Role for Glue/Databricks: Create a role that allows these services to read/write to S3
resource "aws_iam_role" "data_processing_role" {
  name = "SkyHighDataProcessingRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = [
            "glue.amazonaws.com",
          ]
        }
      }
    ]
  })
}

# 8. Attach S3 Full Access to the Role (For learning purposes; in prod, we'd restrict to this specific bucket)
resource "aws_iam_role_policy_attachment" "role_s3_access" {
  role       = aws_iam_role.data_processing_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# 9. Output: Print the bucket name to the terminal so we know what it is!
output "s3_bucket_name" {
  value       = aws_s3_bucket.skyhigh_lake.bucket
  description = "The name of the created S3 bucket"
}