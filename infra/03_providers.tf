# providers.tf: provider blocks
provider "aws" {
  region = var.aws_region

  # default tags  
  default_tags {
    tags = {
      Project     = var.app_name
      Environment = var.env
      ManagedBy   = "terraform"
    }
  }
}
