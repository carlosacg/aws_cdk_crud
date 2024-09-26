import json
import os
from typing import Any, Dict

import boto3

# Initialize DynamoDB resource and table
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler to delete a task item from DynamoDB.

    :param event: The event dictionary containing the HTTP request data, including the taskId in path parameters.
    :param context: The context object, containing runtime information for the Lambda function.
    :return: A dictionary with the HTTP status code for the deletion operation.
    """
    # Extract taskId from the path parameters
    task_id: str = event["pathParameters"]["taskId"]

    # Delete the item from the DynamoDB table
    table.delete_item(Key={"taskId": task_id})

    # Return a success response with a 204 No Content status
    return {
        "statusCode": 204,
        "body": json.dumps({}),  # Include empty body to comply with HTTP standard
    }
