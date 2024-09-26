import json
import os

import boto3
import pytest
from moto import mock_dynamodb2

from lambda_functions import delete_task


@pytest.fixture
def dynamodb_setup():
    """Fixture to set up DynamoDB for testing."""
    with mock_dynamodb2():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName=os.environ["TABLE_NAME"],
            KeySchema=[{"AttributeName": "taskId", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "taskId", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        yield
        table.delete()


def test_delete_task(dynamodb_setup):
    """Test the delete_task Lambda function."""
    # Insert a sample task
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table(os.environ["TABLE_NAME"])
    table.put_item(
        Item={
            "taskId": "123",
            "title": "Test Task",
            "description": "This is a test task.",
            "status": "Pending",
        }
    )

    event = {"pathParameters": {"taskId": "123"}}

    response = delete_task.lambda_handler(event, None)

    assert response["statusCode"] == 204

    # Verify that the task was deleted
    response = table.get_item(Key={"taskId": "123"})
    assert "Item" not in response


def test_delete_task_not_found(dynamodb_setup):
    """Test deleting a task that does not exist."""
    event = {"pathParameters": {"taskId": "non-existent-id"}}

    response = delete_task.lambda_handler(event, None)

    assert (
        response["statusCode"] == 204
    )  # No error should be thrown for non-existent item
