locals {
  account_id = data.aws_caller_identity.current.account_id
  #   partition              = data.aws_partition.this.partition
  #   region                 = data.aws_region.this.name
  #   region_name_tokenized  = split("-", local.region)
  #   region_short           = "${substr(local.region_name_tokenized[0], 0, 2)}${substr(local.region_name_tokenized[1], 0, 1)}${local.region_name_tokenized[2]}"
  #   bedrock_model_arn      = "arn:${local.partition}:bedrock:${local.region}::foundation-model/${coalesce(var.kb_model_id, "amazon.titan-embed-text-v2:0")}"
  #   bedrock_kb_name        = coalesce(var.kb_name, "resourceKB")
  #   image_tag              = formatdate("YYYYMMDDhhmmss", timestamp())
  #   kb_oss_collection_name = coalesce(var.kb_oss_collection_name, "bedrock-resource-kb")
}