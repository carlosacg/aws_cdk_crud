# Serverless Task CRUD API

This project is an AWS CDK application that creates a serverless CRUD API for managing tasks using AWS Lambda, DynamoDB, and API Gateway.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Setup](#setup)
- [Deployment](#deployment)
- [Usage](#usage)
- [Testing](#testing)
- [License](#license)

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
