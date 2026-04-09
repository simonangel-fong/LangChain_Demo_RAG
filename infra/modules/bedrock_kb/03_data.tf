data "aws_caller_identity" "this" {}

data "aws_partition" "this" {}

data "aws_region" "this" {}

data "aws_s3_bucket" "resource_kb" {
  bucket = var.kb_s3_bucket_name_prefix
}

data "aws_bedrock_foundation_model" "kb" {
  model_id = local.bedrock_model_arn
}
