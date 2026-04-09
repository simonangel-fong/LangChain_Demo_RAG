locals {
  account_id     = data.aws_caller_identity.current.account_id
  bedrock_region = var.bedrock_region != "" ? var.bedrock_region : var.aws_region
}