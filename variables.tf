# För att sätta dina egna värden och slippa skriva in dem varje körning
# skapa en fil som heter terraform.tfvars
#  referens: https://developer.hashicorp.com/terraform/tutorials/configuration-language/variables#assign-values-with-a-file

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
