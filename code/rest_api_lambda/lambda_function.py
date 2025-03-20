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
            print(f"[404] Item '{item_id}' not found!")
            return {"statusCode": 404, "body": "Item not found"}

        print(f"[200] Item '{item_id}' found! Value: {response["Item"]["data"]}")
        return {
            "statusCode": 200,
            "body": response["Item"]["data"]
        }
    
    except Exception as e:
        print(f"[500] Exception caught {e}")
        return {"statusCode": 500, "body": "Internal Server Error"}