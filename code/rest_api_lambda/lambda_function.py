import json
import os
import boto3
from log_helper import get_request_logger

# Hämta URL från miljövariabler (som sätts av OpenTofu)
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    request_logger, correlation_id = get_request_logger(event)

    query_params = event.get("queryStringParameters", {})
    item_id = query_params.get("id")

    request_logger.info("Fetching data from DynamoDB", extra={"item_id": item_id})

    try:
        response = dynamodb.get_item(
            TableName=DYNAMODB_TABLE,
            Key={"id": {"N": str(item_id)}}
        )
        item = response.get("Item")

        if not item:
            request_logger.warning("No data found", extra={"item_id": item_id})
            return {"statusCode": 404, "body": json.dumps({"error": "No data found", "correlation_id": correlation_id})}

        request_logger.info("Data retrieved successfully", extra={"item_id": item_id, "data": item})
        return {"statusCode": 200, "body": json.dumps(item)}

    except Exception as e:
        request_logger.error("Error fetching data", extra={"error": str(e), "item_id": item_id}, exc_info=True)
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error", "correlation_id": correlation_id})}