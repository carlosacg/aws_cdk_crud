from typing import Any

from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as lambda_
from aws_cdk import core


class TaskCrudStack(core.Stack):
    """
    AWS CDK stack to create a serverless CRUD API for managing tasks.
    This stack includes a DynamoDB table, Lambda functions, and API Gateway.
    """

    def __init__(self, scope: core.Construct, id: str, **kwargs: Any) -> None:
        """
        Initialize the TaskCrudStack.

        :param scope: The scope in which this stack is defined.
        :param id: The unique identifier for this stack.
        :param kwargs: Additional keyword arguments for the stack.
        """
        super().__init__(scope, id, **kwargs)

        # Create DynamoDB table
        table: dynamodb.Table = dynamodb.Table(
            self,
            "TasksTable",
            partition_key=dynamodb.Attribute(
                name="taskId", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Create Lambda functions for CRUD operations

        create_task_lambda: lambda_.Function = lambda_.Function(
            self,
            "CreateTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="create_task.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions"),
            environment={"TABLE_NAME": table.table_name},
        )

        get_task_lambda: lambda_.Function = lambda_.Function(
            self,
            "GetTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="get_task.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions"),
            environment={"TABLE_NAME": table.table_name},
        )

        update_task_lambda: lambda_.Function = lambda_.Function(
            self,
            "UpdateTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="update_task.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions"),
            environment={"TABLE_NAME": table.table_name},
        )

        delete_task_lambda: lambda_.Function = lambda_.Function(
            self,
            "DeleteTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="delete_task.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions"),
            environment={"TABLE_NAME": table.table_name},
        )

        # Grant the Lambda functions access to the DynamoDB table
        table.grant_read_write_data(create_task_lambda)
        table.grant_read_write_data(get_task_lambda)
        table.grant_read_write_data(update_task_lambda)
        table.grant_read_write_data(delete_task_lambda)

        # Create API Gateway and connect the Lambda functions
        api: apigateway.RestApi = apigateway.RestApi(self, "TasksApi")

        tasks: apigateway.Resource = api.root.add_resource("tasks")
        tasks.add_method("POST", apigateway.LambdaIntegration(create_task_lambda))

        tasks_id: apigateway.Resource = tasks.add_resource("{taskId}")
        tasks_id.add_method("GET", apigateway.LambdaIntegration(get_task_lambda))
        tasks_id.add_method("PUT", apigateway.LambdaIntegration(update_task_lambda))
        tasks_id.add_method("DELETE", apigateway.LambdaIntegration(delete_task_lambda))
