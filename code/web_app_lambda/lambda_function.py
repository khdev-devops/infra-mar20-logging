import requests
import random
import os

# Hämta URL från miljövariabler (som sätts av OpenTofu)
FETCH_API_URL = os.environ.get("FETCH_API_URL")

def lambda_handler(event, context):
    item_id = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])

    print("Fetching item from API...")  # Ingen info om vilket ID som används

    response = requests.get(f"{FETCH_API_URL}?id={item_id}")
    
    # If the request fails (not 200 OK), return an error page
    if response.status_code != 200:
        return {
            "statusCode": 200,  # Still returning 200 to avoid AWS Lambda errors
            "headers": {"Content-Type": "text/html"},
            "body": "<html><body><h1>Something went wrong</h1></body></html>"
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": f"<html><body><h1>Data: {response.text}</h1></body></html>"
    }