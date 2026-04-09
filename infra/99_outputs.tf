output "knowledge_base_id" {
  value       = module.bedrock_kb.knowledge_base_id
  description = "The ID of the Bedrock Knowledge Base"
}

output "knowledge_base_arn" {
  value       = module.bedrock_kb.knowledge_base_arn
  description = "The ARN of the Bedrock Knowledge Base"
}

output "oss_collection_endpoint" {
  value       = module.bedrock_kb.oss_collection_endpoint
  description = "The OpenSearch Serverless collection endpoint"
}
