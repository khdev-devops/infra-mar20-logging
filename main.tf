terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_iam_role" "lambda_role" {
  name = "Student-LambdaLimitedExecution"
}

# Skapa DynamoDB-tabell
resource "aws_dynamodb_table" "data_table" {
  name         = "ExampleTable"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "N"
  }
}

locals {
  fruit_map = {
    "1"  = "Apple"
    "2"  = "Banana"
    "3"  = "Cherry"
    "4"  = "Date"
    "50" = "Elderberry"
    "6"  = "Fig"
    "7"  = "Grape"
    "8"  = "Honeydew"
    "9"  = "Indian Fig"
  }
}

resource "aws_dynamodb_table_item" "items" {
  for_each   = local.fruit_map
  table_name = aws_dynamodb_table.data_table.name
  hash_key   = "id"

  item = jsonencode({
    id   = { N = each.key }
    data = { S = each.value }
  })
}


# Lambda för att hämta data från DynamoDB
resource "aws_lambda_function" "rest_api_lambda" {
  function_name    = "mar20-rest-api"
  role             = data.aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.13"
  filename         = "${data.archive_file.rest_api_lambda_archive.output_path}"
  source_code_hash = data.archive_file.rest_api_lambda_archive.output_base64sha256

  timeout          = 2

  environment {
    variables = {
      LOG_LEVEL = var.log_level
      DYNAMODB_TABLE = aws_dynamodb_table.data_table.name
    }
  }
}

resource "null_resource" "package_rest_api_lambda" {
  provisioner "local-exec" {
    command = <<EOT
      rm -rf ${path.module}/package_rest_api_lambda
      mkdir -p ${path.module}/package_rest_api_lambda
      cp -r ${path.module}/code/rest_api_lambda/* ${path.module}/package_rest_api_lambda/
      pip install -r ${path.module}/code/rest_api_lambda/requirements.txt -t ${path.module}/package_rest_api_lambda
      cd ${path.module}/package_rest_api_lambda && zip -r ${path.module}/rest_api_lambda.zip .
    EOT
  }

  triggers = {
    always_run = timestamp()
  }
}

data "archive_file" "rest_api_lambda_archive" {  
  type        = "zip"  
  source_dir  = "${path.module}/package_rest_api_lambda"
  output_path = "${path.module}/rest_api_lambda.zip"
  depends_on  = [null_resource.package_rest_api_lambda]
}

# Function URL för FetchDataFunction
resource "aws_lambda_function_url" "rest_api_url" {
  function_name = aws_lambda_function.rest_api_lambda.function_name
  authorization_type = "NONE"
}

# Lambda för att generera en webb-sida
resource "aws_lambda_function" "web_app_lambda" {
  function_name    = "mar20-web-app"
  role             = data.aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.13"
  filename         = "${data.archive_file.web_app_lambda_archive.output_path}"
  source_code_hash = data.archive_file.web_app_lambda_archive.output_base64sha256
  timeout          = 2

  environment {
    variables = {
      LOG_LEVEL = var.log_level
      FETCH_API_URL = aws_lambda_function_url.rest_api_url.function_url
    }
  }
}

resource "null_resource" "package_web_app_lambda" {
  provisioner "local-exec" {
    command = <<EOT
      rm -rf ${path.module}/package_web_app_lambda
      mkdir -p ${path.module}/package_web_app_lambda
      cp -r ${path.module}/code/web_app_lambda/* ${path.module}/package_web_app_lambda/
      pip install -r ${path.module}/code/web_app_lambda/requirements.txt -t ${path.module}/package_web_app_lambda
      cd ${path.module}/package_web_app_lambda && zip -r ${path.module}/web_app_lambda.zip .
    EOT
  }

  triggers = {
    always_run = timestamp()
  }
}

data "archive_file" "web_app_lambda_archive" {  
  type        = "zip"  
  source_dir  = "${path.module}/package_web_app_lambda"
  output_path = "${path.module}/web_app_lambda.zip"
  depends_on  = [null_resource.package_web_app_lambda]
}

# Function URL för GeneratePageFunction
resource "aws_lambda_function_url" "web_app_url" {
  function_name      = aws_lambda_function.web_app_lambda.function_name
  authorization_type = "NONE"
}
