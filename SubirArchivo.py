import boto3
import json
import base64
import binascii
import mimetypes
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")

        bucket = body["bucket"]
        directorio = body["directorio"].strip("/")
        nombre = body["nombre_archivo"]
        contenido = body["contenido_base64"]

        archivo = base64.b64decode(
            contenido,
            validate=True
        )

        ruta = f"{directorio}/{nombre}" if directorio else nombre
        tipo, _ = mimetypes.guess_type(nombre)

        s3.put_object(
            Bucket=bucket,
            Key=ruta,
            Body=archivo,
            ContentType=tipo or "application/octet-stream"
        )

        return {
            "statusCode": 201,
            "body": json.dumps({
                "mensaje": "Archivo subido correctamente",
                "bucket": bucket,
                "ruta": ruta,
                "bytes": len(archivo)
            })
        }

    except (KeyError, ValueError, TypeError, binascii.Error) as e:
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