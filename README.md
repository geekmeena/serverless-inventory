# Serverless Inventory System

A serverless inventory management project built with **AWS CDK and Python**.

The application processes inventory data uploaded as CSV files, stores inventory records in Amazon DynamoDB, and sends notifications when an item's stock reaches zero.

## Architecture

```text
CSV Upload
    │
    ▼
Amazon S3
    │
    ▼
Lambda - LoadInventory
    │
    ▼
Amazon DynamoDB
    │
    ▼
DynamoDB Stream
    │
    ▼
Lambda - CheckInventory
    │
    ▼
Amazon SNS
    │
    ▼
Stock Alert
```

## How It Works

1. An inventory CSV file is uploaded to an Amazon S3 bucket.
2. S3 triggers the `LoadInventory` Lambda function.
3. The Lambda function processes the CSV data and stores inventory records in DynamoDB.
4. DynamoDB Streams capture changes to inventory records.
5. The `CheckInventory` Lambda function checks updated stock levels.
6. When an item's stock reaches zero, a notification is published to Amazon SNS.

## AWS Services

- **Amazon S3** – stores uploaded inventory CSV files
- **AWS Lambda** – processes inventory data and checks stock levels
- **Amazon DynamoDB** – stores inventory records
- **DynamoDB Streams** – captures inventory record changes
- **Amazon SNS** – publishes zero-stock notifications
- **AWS CDK (Python)** – defines the infrastructure as code

## Project Structure

```text
serverless-inventory/
├── serverless_inventory/
│   ├── lambdas/
│   │   ├── load_inventory.py
│   │   └── check_inventory.py
│   └── serverless_inventory_stack.py
├── tests/
├── app.py
├── cdk.json
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
└── README.md
```

## Local Setup

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Bootstrap AWS CDK

```bash
cdk bootstrap
```

### 4. Review the generated infrastructure

```bash
cdk synth
```

### 5. Deploy

```bash
cdk deploy
```

> Deployment creates AWS resources and may incur AWS charges.

## Example Inventory Data

```csv
store,item,count
Berlin,Amazon Tap,15
Berlin,Echo Dot,12
Berlin,Echo Plus,0
```

Uploading inventory data to the configured S3 bucket triggers the processing workflow. Inventory records are stored in DynamoDB and zero-stock items can trigger SNS notifications.

## Skills Demonstrated

- AWS serverless architecture
- Infrastructure as Code with AWS CDK
- Python
- Event-driven architecture
- AWS Lambda
- Amazon S3
- Amazon DynamoDB and DynamoDB Streams
- Amazon SNS