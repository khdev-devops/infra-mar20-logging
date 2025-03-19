import json
import requests
import random
import os
from log_helper import get_request_logger

# Hämta URL från miljövariabler (som sätts av OpenTofu)
FETCH_API_URL = os.environ.get("FETCH_API_URL")

def lambda_handler(event, context):
    # Get request-scoped logger and correlation ID from helper
    request_logger, correlation_id = get_request_logger(event)

    item_id = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])

    try:
        headers = {"X-Correlation-ID": correlation_id}
        request = f"{FETCH_API_URL}?id={item_id}"
        request_logger.info(f"Calling API", extra={"request_url":request, "headers":headers})
        response = requests.get(request, headers=headers)

        if response.status_code != 200:
            request_logger.warning("API returned non-200 status", extra={"request_url":request, "status_code":response.status_code, "response":response.text})
            return {"statusCode": 200, "headers": {"Content-Type": "text/html"}, "body": f"<html><body><h1>Something went wrong (ID: {item_id})</h1></body></html>"}

        request_logger.info("Data retrieved successfully", extra={"item_id":item_id, "data":response.text})
        return {"statusCode": 200, "headers": {"Content-Type": "text/html"}, "body": f"<html><body><h1>Data: {response.text}</h1></body></html>"}

    except Exception as e:
        request_logger.error(f"Error calling API: {e}", extra={"request_url":request}, exc_info=True)
        return {"statusCode": 200, "headers": {"Content-Type": "text/html"}, "body": f"<html><body><h1>Something went wrong (ID: {item_id})</h1></body></html>"}