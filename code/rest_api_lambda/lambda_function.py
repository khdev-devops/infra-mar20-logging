import json
import boto3
import os

# Hämta URL från miljövariabler (som sätts av OpenTofu)
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE")

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    print("Fetching data from DynamoDB")  # Dålig loggning (ingen kontext)
    
    try:
        item_id = int(event["queryStringParameters"]["id"])
        response = dynamodb.get_item(
            TableName=DYNAMODB_TABLE,
            Key={"id": {"N": str(item_id)}}
        )

        if "Item" not in response:
            print("Item not found!")  # Ingen info om vilket ID som saknas
            return {"statusCode": 404, "body": "Item not found"}

        return {
            "statusCode": 200,
            "body": response["Item"]["data"]
        }
    
    except Exception as e:
        print("Something went wrong!")  # Ingen detaljerad felhantering
        return {"statusCode": 500, "body": "Internal Server Error"}