import json
import os

import boto3
import pytest
from moto import mock_dynamodb2

from lambda_functions import create_task


@pytest.fixture
def dynamodb_setup():
    """Fixture to set up DynamoDB for testing."""
    with mock_dynamodb2():
        # Crear tabla DynamoDB para las pruebas
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName=os.environ["TABLE_NAME"],
            KeySchema=[{"AttributeName": "taskId", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "taskId", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        yield  # Permite ejecutar las pruebas
        table.delete()  # Limpia la tabla después de las pruebas


def test_create_task(dynamodb_setup):
    """Test the create_task Lambda function."""
    event = {
        "body": json.dumps(
            {
                "title": "Test Task",
                "description": "This is a test task.",
                "status": "Pending",
            }
        )
    }

    response = create_task.lambda_handler(event, None)

    assert response["statusCode"] == 201
    item = json.loads(response["body"])
    assert "taskId" in item
    assert item["title"] == "Test Task"
    assert item["description"] == "This is a test task."
    assert item["status"] == "Pending"
