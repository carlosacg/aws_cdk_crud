import json
import os

import boto3
import pytest
from moto import mock_dynamodb2

from lambda_functions import update_task


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


def test_update_task(dynamodb_setup):
    """Test the update_task Lambda function."""
    # Insert a sample task
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table(os.environ["TABLE_NAME"])
    table.put_item(
        Item={
            "taskId": "123",
            "title": "Old Task",
            "description": "Old description",
            "status": "Pending",
        }
    )

    event = {
        "pathParameters": {"taskId": "123"},
        "body": json.dumps(
            {
                "title": "Updated Task",
                "description": "Updated description",
                "status": "Completed",
            }
        ),
    }

    response = update_task.lambda_handler(event, None)

    assert response["statusCode"] == 200
    updated_item = json.loads(response["body"])
    assert updated_item["title"] == "Updated Task"
    assert updated_item["description"] == "Updated description"
    assert updated_item["status"] == "Completed"


def test_update_task_not_found(dynamodb_setup):
    """Test updating a task that does not exist."""
    event = {
        "pathParameters": {"taskId": "non-existent-id"},
        "body": json.dumps(
            {
                "title": "Updated Task",
                "description": "Updated description",
                "status": "Completed",
            }
        ),
    }

    response = update_task.lambda_handler(event, None)

    assert response["statusCode"] == 404
