# Knowledge base resource role
resource "aws_iam_role" "bedrock_kb_resource_kb" {
  name               = "${local.bedrock_kb_name}-bedrock_kb"
  assume_role_policy = data.aws_iam_policy_document.bedrock_kb_assume_role.json
}

data "aws_iam_policy_document" "bedrock_kb_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["bedrock.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [local.account_id]
    }
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:${local.partition}:bedrock:${local.region}:${local.account_id}:knowledge-base/*"]
    }
  }
}

# Knowledge base bedrock invoke policy
resource "aws_iam_role_policy" "bedrock_kb_resource_kb_model" {
  name   = "${local.bedrock_kb_name}-bedrock-kb-model"
  role   = aws_iam_role.bedrock_kb_resource_kb.name
  policy = data.aws_iam_policy_document.bedrock_kb_model.json
}

data "aws_iam_policy_document" "bedrock_kb_model" {
  statement {
    actions   = ["bedrock:InvokeModel"]
    effect    = "Allow"
    resources = [local.bedrock_model_arn]
  }
}

# Knowledge base S3 policy
resource "aws_iam_role_policy" "bedrock_kb_resource_kb_s3" {
  name   = "${local.bedrock_kb_name}-bedrock-kb-s3"
  role   = aws_iam_role.bedrock_kb_resource_kb.name
  policy = data.aws_iam_policy_document.bedrock_kb_s3.json
}

data "aws_iam_policy_document" "bedrock_kb_s3" {
  statement {
    sid       = "S3ListBucketStatement"
    actions   = ["s3:ListBucket"]
    effect    = "Allow"
    resources = [data.aws_s3_bucket.resource_kb.arn]
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceAccount"
      values   = [local.account_id]
    }
  }

  statement {
    sid       = "S3GetObjectStatement"
    actions   = ["s3:GetObject"]
    effect    = "Allow"
    resources = ["${data.aws_s3_bucket.resource_kb.arn}/*"]
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceAccount"
      values   = [local.account_id]
    }
  }
}

# Knowledge base opensearch access policy
resource "aws_iam_role_policy" "bedrock_kb_resource_kb_oss" {
  name   = "${local.bedrock_kb_name}-bedrock-kb-oss"
  role   = aws_iam_role.bedrock_kb_resource_kb.name
  policy = data.aws_iam_policy_document.bedrock_kb_oss.json
}

data "aws_iam_policy_document" "bedrock_kb_oss" {
  statement {
    actions   = ["aoss:APIAccessAll"]
    effect    = "Allow"
    resources = [aws_opensearchserverless_collection.resource_kb.arn]
  }
}
