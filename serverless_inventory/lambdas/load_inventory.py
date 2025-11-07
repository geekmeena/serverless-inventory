import json
import urllib.parse
import boto3
import csv
import os

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    local_file = '/tmp/inventory.csv'
    s3.Bucket(bucket).download_file(key, local_file)

    inserted = 0
    with open(local_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            table.put_item(Item={
                "Store": row["store"],
                "Item": row["item"],
                "Count": int(row["count"])
            })
            inserted += 1

    return {"message": f"Inserted {inserted} rows"}
