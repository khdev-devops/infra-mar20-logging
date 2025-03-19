import json
import os
import uuid
from datetime import datetime
from loguru import logger

# Global Log Setup
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logger.remove()

# Custom log serializer to include timestamps
def custom_json_serializer(message):
    record = message.record
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "correlation_id": record["extra"].get("correlation_id"),
        "request_ip": record["extra"].get("request_ip"),
        "user_agent": record["extra"].get("user_agent"),
        "lambda_name": record["extra"].get("lambda_name"),
    }
    # Merge any additional `extra` fields dynamically
    log_entry.update(record["extra"].get("extra", {}))  
    return json.dumps(log_entry)

# custom serializer to Loguru
logger.add(lambda msg: print(custom_json_serializer(msg)), level=LOG_LEVEL, serialize=True)

# Bind global metadata
logger = logger.bind(lambda_name=os.getenv("AWS_LAMBDA_FUNCTION_NAME", "unknown_lambda"))

def get_request_logger(event):
    """
    Extract request context and create a child logger specific to this request.
    Returns the logger AND the correlation ID (as it may have been generated).
    """
    correlation_id = event.get("headers", {}).get("x-correlation-id") or str(uuid.uuid4())

    ctx = {
        "correlation_id": correlation_id,
        "request_ip": event.get("requestContext", {}).get("http", {}).get("sourceIp", "Unknown"),
        "user_agent": event.get("headers", {}).get("user-agent", "Unknown"),
    }

    return logger.bind(**ctx), correlation_id