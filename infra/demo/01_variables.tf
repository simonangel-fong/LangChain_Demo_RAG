# variables.tf: Input Variables

# ##############################
# APP
# ##############################
variable "app_name" {
  type    = string
  default = "bedrock-knowledge-base"
}

variable "env" {
  type    = string
  default = "demo"
}

# ##############################
# AWS
# ##############################
variable "aws_region" { type = string }

# ##############################
# Bedrock
# ##############################
variable "embedding_model" {
  type    = string
  default = "amazon.titan-embed-text-v2:0"
}

##############################
# AWS lambda
##############################
variable "lambda_file_path" {
  description = "Lambda function source file path"
  type        = string
  default     = "../../app/lambda/main.py"
}

variable "lambda_zip_path" {
  description = "Lambda function zip file path"
  type        = string
  default     = "../../app/lambda/main.zip"
}

variable "lambda_handler" {
  description = "AWS lambda function handler"
  type        = string
  default     = "main.lambda_handler"
}

variable "lambda_runtime" {
  description = "AWS lambda function runtime"
  type        = string
  default     = "python3.12"
}

##############################
# Bedrock Configuration
##############################
variable "bedrock_model_id" {
  description = "The Bedrock model ID for text generation"
  type        = string
  # default     = "us.amazon.nova-2-lite-v1:0"
  default = "amazon.nova-lite-v1:0"
}

variable "bedrock_inference_profile_arn" {
  description = "ARN of the Bedrock inference profile (if using provisioned throughput)"
  type        = string
  default     = ""
}

variable "bedrock_region" {
  description = "AWS region for Bedrock service (defaults to aws_region)"
  type        = string
  default     = ""
}

##############################
# AWS API Gateway
##############################
variable "apigw_path" {
  description = "API Gateway path"
  type        = string
  default     = "app"
}
