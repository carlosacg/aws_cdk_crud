# Serverless Task CRUD API

This project is an AWS CDK application that creates a serverless CRUD API for managing tasks using AWS Lambda, DynamoDB, and API Gateway.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Setup](#setup)
- [Deployment](#deployment)
- [Usage](#usage)

## Features

- Create, read, update, and delete tasks.
- Uses AWS Lambda functions to handle API requests.
- Data is stored in DynamoDB.
- Exposes a REST API using API Gateway.

## Architecture

This project utilizes the following AWS services:

- **AWS Lambda**: Executes code in response to HTTP requests.
- **Amazon API Gateway**: Manages the RESTful API endpoints.
- **Amazon DynamoDB**: A fully managed NoSQL database to store task data.

## Requirements

- AWS Account
- AWS CLI configured with appropriate permissions
- Node.js and npm
- AWS CDK installed globally:
  ```bash
  npm install -g aws-cdk
  ```

## Setup

- Clone this repository:
  ```bash
  git clone https://github.com/carlosacg/aws_cdk_crud.git
  cd aws_cdk_crud
  ```
- Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```

## Deployment

- Synthesize the CloudFormation template:
  ```bash
  cdk synth
  ```
- Deploy the stack:
  ```bash
  cdk deploy
  ```
- After deployment, the API Gateway URL will be displayed in the terminal. You can use this URL to interact with the API.

## Usage
# Endpoints
- Create Task
  ```bash
  #Request body
  {
    "title": "Task Title",
    "description": "Task Description",
    "status": "pending"
  }
  ```

- Get Task
  ```bash
  GET /tasks/{taskId}
  ```

- Update Task
  ```bash
  PUT /tasks/{taskId}
  #Request body
  {
    "title": "Updated Title",
    "description": "Updated Description",
    "status": "completed"
  }
  ```

- Delete Task
  ```bash
  DELETE /tasks/{taskId}
  ```