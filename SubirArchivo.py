import boto3
import json
import base64
import binascii
import os
import mimetypes
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
PREFIX = os.environ["BUCKET_PREFIX"]

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")

        bucket = body["bucket"]
        directorio = body["directorio"].strip("/")
        nombre = body["nombre_archivo"]
        contenido = body["contenido_base64"]

        if not bucket.startswith(PREFIX):
            raise ValueError("Bucket no permitido")

        if (
            not directorio
            or not nombre
            or "/" in nombre
            or "\\" in nombre
            or any(p in (".", "..") for p in directorio.split("/"))
        ):
            raise ValueError("Ruta o nombre de archivo inválido")

        archivo = base64.b64decode(contenido, validate=True)
        ruta = f"{directorio}/{nombre}"

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