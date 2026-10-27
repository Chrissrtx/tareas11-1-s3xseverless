import boto3
import json
import os
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
PREFIX = os.environ["BUCKET_PREFIX"]

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")

        bucket = body["bucket"]
        directorio = body["directorio"].strip("/")

        if not bucket.startswith(PREFIX) or not directorio:
            raise ValueError("Bucket o directorio inválido")

        if any(p in (".", "..") for p in directorio.split("/")):
            raise ValueError("Ruta no permitida")

        ruta = directorio + "/"

        s3.put_object(
            Bucket=bucket,
            Key=ruta,
            Body=b""
        )

        return {
            "statusCode": 201,
            "body": json.dumps({
                "mensaje": "Directorio creado",
                "bucket": bucket,
                "directorio": ruta
            })
        }

    except (KeyError, ValueError, TypeError) as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

    except ClientError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": e.response["Error"]["Code"]
            })
        }