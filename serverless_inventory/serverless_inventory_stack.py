from aws_cdk import (
    Stack,
    Duration,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_sns as sns,
    aws_lambda_event_sources as event_sources,
)
from constructs import Construct

class ServerlessInventoryStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket (for CSV uploads)
        bucket = s3.Bucket(
            self, "InventoryUploadBucket",
            versioned=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # DynamoDB table (with stream for Lambda)
        inventory_table = dynamodb.Table(
            self, "InventoryTable",
            partition_key=dynamodb.Attribute(
                name="Store", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="Item", type=dynamodb.AttributeType.STRING
            ),
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        # SNS Topic (for sending alerts)
        topic = sns.Topic(
            self, 
            "NoStockTopic",
            display_name="Inventory Low/Zero Stock Alerts"
        )

        # Lambda #1: Load Inventory (S3 → DynamoDB)
        load_inventory_lambda = lambda_.Function(
            self, 
            "LoadInventoryLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="load_inventory.lambda_handler",
            code=lambda_.Code.from_asset("serverless_inventory/lambdas"),
            timeout=Duration.seconds(30),
            environment={
                "TABLE_NAME": inventory_table.table_name
            }
        )

        # Give Lambda permission to read S3 + write DynamoDB
        bucket.grant_read(load_inventory_lambda)
        inventory_table.grant_write_data(load_inventory_lambda)

        # Trigger Lambda when CSV uploaded to S3
        load_inventory_lambda.add_event_source(
            event_sources.S3EventSource(
                bucket,
                events=[s3.EventType.OBJECT_CREATED],
                filters=[s3.NotificationKeyFilter(suffix=".csv")]
            )
        )

        # Lambda #2: Check Inventory (DynamoDB Stream → SNS)
        check_inventory_lambda = lambda_.Function(
            self,
            "CheckInventoryLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="check_inventory.lambda_handler",
            code=lambda_.Code.from_asset("serverless_inventory/lambdas"),
            timeout=Duration.seconds(30),
            environment={
                "SNS_TOPIC_ARN": topic.topic_arn
            }
        )

        #  Give Lambda permission to publish to SNS
        topic.grant_publish(check_inventory_lambda)

        # Trigger when DynamoDB row inserted
        check_inventory_lambda.add_event_source(
            event_sources.DynamoEventSource(
                inventory_table,
                starting_position=lambda_.StartingPosition.LATEST,
                batch_size=1
            )
        )

