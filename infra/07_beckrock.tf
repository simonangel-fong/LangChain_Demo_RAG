module "bedrock_kb" {
  source = "./modules/bedrock_kb"

  kb_model_id              = var.embedding_model
  kb_name                  = var.app_name
  kb_s3_bucket_name_prefix = aws_s3_bucket.bucket.bucket
  kb_oss_collection_name   = "${var.app_name}-kb"
}
