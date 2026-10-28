
import boto3
import json
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        nombre_bucket = body["bucket"]

        response = s3.list_objects_v2(
            Bucket=nombre_bucket
        )

        lista = [
            obj["Key"]
            for obj in response.get("Contents", [])
        ]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "bucket": nombre_bucket,
                "lista_objetos": lista
            })
        }

    except (KeyError, ValueError, TypeError):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Debe proporcionar un bucket válido"
            })
        }

    except ClientError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": e.response["Error"]["Code"]
            })
        }
