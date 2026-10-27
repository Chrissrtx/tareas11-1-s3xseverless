import boto3
import json
import os
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
REGION = os.environ.get("AWS_REGION", "us-east-1")
PREFIX = os.environ["BUCKET_PREFIX"]

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        bucket = body["bucket"]

        if not bucket.startswith(PREFIX):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": f"El bucket debe empezar con {PREFIX}"
                })
            }

        params = {"Bucket": bucket}

        if REGION != "us-east-1":
            params["CreateBucketConfiguration"] = {
                "LocationConstraint": REGION
            }

        s3.create_bucket(**params)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "mensaje": "Bucket creado correctamente",
                "bucket": bucket
            })
        }

    except (KeyError, ValueError, TypeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "JSON o bucket inválido"})
        }

    except ClientError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": e.response["Error"]["Code"]
            })
        }