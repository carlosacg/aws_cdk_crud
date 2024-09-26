import json
import os
from typing import Any, Dict

import boto3

# Initialize DynamoDB resource and table
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler to retrieve a task item from DynamoDB.

    :param event: The event dictionary containing the HTTP request data, including the taskId in path parameters.
    :param context: The context object, containing runtime information for the Lambda function.
    :return: A dictionary with the HTTP status code and the task item if found, or an error message if not found.
    """
    # Extract taskId from the path parameters
    task_id: str = event["pathParameters"]["taskId"]

    # Retrieve the item from the DynamoDB table
    response = table.get_item(Key={"taskId": task_id})
    item = response.get("Item")

    # Check if the item was found
    if not item:
        return {"statusCode": 404, "body": json.dumps({"error": "Task not found"})}

    # Return the found item with a 200 OK status
    return {"statusCode": 200, "body": json.dumps(item)}
