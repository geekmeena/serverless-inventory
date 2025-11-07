import boto3
import os
import json

sns = boto3.client("sns")
topic_arn = os.environ["SNS_TOPIC_ARN"]

def lambda_handler(event, context):
    print("Event:", json.dumps(event))

    for record in event.get("Records", []):
        if record.get("eventName") != "INSERT":
            continue

        new = record["dynamodb"]["NewImage"]
        store = new["Store"]["S"]
        item = new["Item"]["S"]
        count = int(new["Count"]["N"])

        if count == 0:
            msg = f"Item '{item}' at store '{store}' is OUT OF STOCK!"
            sns.publish(TopicArn=topic_arn, Message=msg, Subject="Inventory Alert")
            print("ALERT SENT:", msg)
