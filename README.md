**Serverless Inventory System (AWS CDK – Python)**
Overview

The Serverless Inventory System is an automated stock management solution built using AWS CDK (Python).
It enables seamless ingestion of product inventory data from CSV files, stores valid records in DynamoDB, and sends notifications when stock levels reach zero.

The architecture is fully serverless, scalable, and defined using Infrastructure as Code (IaC) with AWS CDK.

## Architecture
Store (CSV Upload)
│
▼
S3 Bucket ──► Lambda (LoadInventory)
│
▼
DynamoDB Table
│
▼
DynamoDB Stream ──► Lambda (CheckInventory)
│
▼
SNS Topic (Email Alerts)

**Features**

Upload inventory files (CSV format) directly to an S3 bucket.

Automatically load and store data in DynamoDB.

Detect zero-stock items in real time.

Notify subscribed users through Amazon SNS.

Infrastructure defined entirely using AWS CDK (Python).

AWS Services Used

AWS Lambda – Processes CSV data and checks inventory.

Amazon S3 – Stores uploaded inventory files.

Amazon DynamoDB – Maintains inventory records.

Amazon SNS – Sends notifications for zero-stock items.

AWS CDK (Python) – Infrastructure as Code.


## Project Structure
serverless_inventory/
│
├── lambdas/
│ ├── load_inventory.py # Lambda to load CSV data from S3 to DynamoDB
│ └── check_inventory.py # Lambda to check stock and trigger SNS
│
├── serverless_inventory_stack.py # Main CDK stack definition
├── app.py # CDK app entry point
├── requirements.txt # Python dependencies
└── README.md # Project documentation

**Setup and Deployment**
1. Clone the Repository
   
2. Set Up a Virtual Environment
   python3 -m venv .venv
   source .venv/bin/activate

3. Install Dependencies
   pip install -r requirements.txt

4. Bootstrap CDK (one-time setup per AWS account)
   cdk bootstrap

5. Deploy the Stack
  cdk deploy

6. Verify Deployment

   S3 Bucket created for CSV uploads

   DynamoDB Table created for inventory data

   SNS Topic created for stock alerts

   Two Lambda functions automatically connected to triggers

**Example CSV Format**
store,item,count
Berlin,Amazon Tap,15
Berlin,Echo Dot,12
Berlin,Echo Plus,0
Uploading a file like this to the S3 bucket will trigger automatic ingestion.
If any item has a count of 0, an SNS email alert will be sent.

**Notifications**

SNS Topic Name: NoStock

Subscribe via:

Email (confirmation required)

SMS or Lambda trigger (optional)

**Author**
Meenakshi Sharma
