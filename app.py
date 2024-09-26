# app.py
from aws_cdk import core

from cdk_infrastructure.task_crud_stack import TaskCrudStack

app = core.App()
TaskCrudStack(app, "TaskCrudStack")
app.synth()
