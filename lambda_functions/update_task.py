import json
import os
from typing import Any, Dict

import boto3

# Initialize DynamoDB resource and table
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler to update a task item in DynamoDB.

    :param event: The event dictionary containing the HTTP request data, including the taskId in path parameters and the update data in the body.
    :param context: The context object, containing runtime information for the Lambda function.
    :return: A dictionary with the HTTP status code and the updated task item.
    """
    # Extract taskId from the path parameters
    task_id: str = event["pathParameters"]["taskId"]

    # Parse the request body to get the updated values
    body: Dict[str, Any] = json.loads(event["body"])

    # Update the item in the DynamoDB table
    response = table.update_item(
        Key={"taskId": task_id},
        UpdateExpression="set title=:t, description=:d, #s=:s",
        ExpressionAttributeValues={
            ":t": body["title"],
            ":d": body["description"],
            ":s": body["status"],
        },
        ExpressionAttributeNames={"#s": "status"},
        ReturnValues="UPDATED_NEW",
    )

    # Return the updated item with a 200 OK status
    return {"statusCode": 200, "body": json.dumps(response["Attributes"])}
