import boto3
import json
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")

        bucket = body["bucket"]
        directorio = body["directorio"].strip("/")

        if not directorio:
            raise ValueError("Directorio vacío")

        ruta = directorio + "/"

        s3.put_object(
            Bucket=bucket,
            Key=ruta,
            Body=b""
        )

        return {
            "statusCode": 201,
            "body": json.dumps({
                "mensaje": "Directorio creado correctamente",
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