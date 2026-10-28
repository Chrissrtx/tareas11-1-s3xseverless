
import boto3
import json
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

def lambda_handler(event, context):
    try:
        response = s3.list_buckets()

        lista = [
            bucket["Name"]
            for bucket in response["Buckets"]
        ]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "lista_buckets": lista
            })
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": e.response["Error"]["Code"]
            })
        }
