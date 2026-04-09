output "knowledge_base_id" {
  value       = aws_bedrockagent_knowledge_base.resource_kb.id
  description = "The ID of the Knowledge Base"
}

output "knowledge_base_arn" {
  value       = aws_bedrockagent_knowledge_base.resource_kb.arn
  description = "The ARN of the Knowledge Base"
}

output "s3_bucket_name" {
  value       = data.aws_s3_bucket.resource_kb.bucket
  description = "The S3 bucket name used as the data source for the Knowledge Base"
}

output "oss_collection_arn" {
  value       = aws_opensearchserverless_collection.resource_kb.arn
  description = "The ARN of the OpenSearch Serverless collection"
}

output "oss_collection_endpoint" {
  value       = aws_opensearchserverless_collection.resource_kb.collection_endpoint
  description = "The endpoint of the OpenSearch Serverless collection"
}
