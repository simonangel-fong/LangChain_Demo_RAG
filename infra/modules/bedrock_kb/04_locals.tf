locals {
  account_id             = data.aws_caller_identity.this.account_id
  partition              = data.aws_partition.this.partition
  region                 = data.aws_region.this.id
  region_name_tokenized  = split("-", local.region)
  region_short           = "${substr(local.region_name_tokenized[0], 0, 2)}${substr(local.region_name_tokenized[1], 0, 1)}${local.region_name_tokenized[2]}"
  bedrock_model_arn      = "arn:${local.partition}:bedrock:${local.region}::foundation-model/${var.kb_model_id}"
  bedrock_kb_name        = var.kb_name
  kb_oss_collection_name = var.kb_oss_collection_name

  # OpenSearch field and index names
  oss_index_name     = "bedrock-knowledge-base-default-index"
  oss_vector_field   = "bedrock-knowledge-base-default-vector"
  oss_text_field     = "AMAZON_BEDROCK_TEXT_CHUNK"
  oss_metadata_field = "AMAZON_BEDROCK_METADATA"
}
