# variables.tf: Input Variables

# ##############################
# APP
# ##############################
variable "app_name" {
  type    = string
  default = "bedrock-knowledge-base"
}

variable "env" {
  type    = string
  default = "demo"
}

# ##############################
# AWS
# ##############################
variable "aws_region" { type = string }
