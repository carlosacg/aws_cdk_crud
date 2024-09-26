import json
import os
import uuid
from typing import Any, Dict

import boto3

# Initialize DynamoDB resource and table
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler for creating a new task item in DynamoDB.

    :param event: The event dictionary containing the HTTP request data.
    :param context: The context object, containing runtime information for the Lambda function.
    :return: A dictionary with the HTTP status code and the newly created task item in JSON format.
    """
    # Generate a unique task ID
    task_id: str = str(uuid.uuid4())

    # Parse the request body
    body: Dict[str, str] = json.loads(event["body"])

    # Define the task item to be inserted in DynamoDB
    item: Dict[str, str] = {
        "taskId": task_id,
        "title": body["title"],
        "description": body["description"],
        "status": body["status"],
    }

    # Insert the item into the DynamoDB table
    table.put_item(Item=item)

    # Return a success response with the created task
    return {
        "statusCode": 201,
        "body": json.dumps(item),
    }
