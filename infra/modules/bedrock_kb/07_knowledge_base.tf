resource "time_sleep" "aws_iam_role_policy_bedrock_kb_resource_kb_oss" {
  create_duration = "20s"
  depends_on      = [aws_iam_role_policy.bedrock_kb_resource_kb_oss]
}

# Knowledge base resource creation
resource "aws_bedrockagent_knowledge_base" "resource_kb" {
  name     = local.bedrock_kb_name
  role_arn = aws_iam_role.bedrock_kb_resource_kb.arn
  knowledge_base_configuration {
    vector_knowledge_base_configuration {
      embedding_model_arn = local.bedrock_model_arn
    }
    type = "VECTOR"
  }
  storage_configuration {
    type = "OPENSEARCH_SERVERLESS"
    opensearch_serverless_configuration {
      collection_arn    = aws_opensearchserverless_collection.resource_kb.arn
      vector_index_name = local.oss_index_name
      field_mapping {
        vector_field   = local.oss_vector_field
        text_field     = local.oss_text_field
        metadata_field = local.oss_metadata_field
      }
    }
  }
  depends_on = [
    aws_iam_role_policy.bedrock_kb_resource_kb_model,
    aws_iam_role_policy.bedrock_kb_resource_kb_s3,
    opensearch_index.resource_kb,
    time_sleep.aws_iam_role_policy_bedrock_kb_resource_kb_oss
  ]
}

resource "aws_bedrockagent_data_source" "resource_kb" {
  knowledge_base_id = aws_bedrockagent_knowledge_base.resource_kb.id
  name              = "${local.bedrock_kb_name}DataSource"
  data_source_configuration {
    type = "S3"
    s3_configuration {
      bucket_arn = data.aws_s3_bucket.resource_kb.arn
    }
  }

  # Only include vector_ingestion_configuration if not using DEFAULT strategy
  dynamic "vector_ingestion_configuration" {
    for_each = var.chunking_strategy != "DEFAULT" ? [1] : []
    content {
      chunking_configuration {
        chunking_strategy = var.chunking_strategy

        dynamic "fixed_size_chunking_configuration" {
          for_each = var.chunking_strategy == "FIXED_SIZE" ? [1] : []
          content {
            max_tokens         = var.fixed_size_max_tokens
            overlap_percentage = var.fixed_size_overlap_percentage
          }
        }

        dynamic "hierarchical_chunking_configuration" {
          for_each = var.chunking_strategy == "HIERARCHICAL" ? [1] : []
          content {
            overlap_tokens = var.hierarchical_overlap_tokens
            level_configuration {
              max_tokens = var.hierarchical_parent_max_tokens
            }
            level_configuration {
              max_tokens = var.hierarchical_child_max_tokens
            }
          }
        }

        dynamic "semantic_chunking_configuration" {
          for_each = var.chunking_strategy == "SEMANTIC" ? [1] : []
          content {
            max_token                       = var.semantic_max_tokens
            buffer_size                     = var.semantic_buffer_size
            breakpoint_percentile_threshold = var.semantic_breakpoint_percentile_threshold
          }
        }
      }
    }
  }
}
