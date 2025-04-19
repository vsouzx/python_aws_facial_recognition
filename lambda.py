from requests_toolbelt.multipart import decoder
from decimal import Decimal
import json
import base64
import boto3
import uuid
import os

s3 = boto3.client('s3')
try:
    # Tentar obter o valor da variável de ambiente
    table_name = os.environ['DYNAMODB_TABLE']
    bucket_name = os.environ['BUCKET_NAME']
except KeyError:
    # Lançar uma exceção personalizada se a variável não estiver configurada
    raise EnvironmentError("A variável de ambiente não está configurada.")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print(f'Event: {event}')

    path = event['path']

    if path == '/register':
        content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')
        
        if not content_type.startswith('multipart/form-data'):
            return {
            'statusCode': 400,
            'body': json.dumps({'message':'Content-Type inválido. Esperado: multipart/form-data'})
            }

        if not event.get("body"):
            return {
                'statusCode': 400,
                'body': json.dumps({'message':'Body inválido. Esperado: multipart/form-data'})
            }

        body = event['body']
        if event.get("isBase64Encoded"):
            body = base64.b64decode(body)
        else:
            body = body.encode('utf-8') 

        print(f'Body: {body}')

        multipart_data = decoder.MultipartDecoder(body, content_type)

        form_data = {}
        for part in multipart_data.parts:
            content_disposition = part.headers[b'Content-Disposition'].decode()
            name = content_disposition.split("name=")[1].split(";")[0].replace('"', '')
            if b'filename' in part.headers[b'Content-Disposition']:
                form_data['photo'] = {
                    'filename': part.headers[b'Content-Disposition'].decode().split('filename=')[1].replace('"', '').strip(),
                    'content': part.content
                }
            else:
                form_data[name] = part.text

        nome = form_data.get('nome')
        print(f'Nome: {nome}')
        photo = form_data.get('photo')
        print(f'Photo: {photo}')

        if not all([nome, photo]):
            return {
                'statusCode': 400,
                'body': json.dumps('Todos os campos são obrigatórios.')
            }
        
        uuid = str(uuid.uuid4())
        
        # S3 - upload da imagem
        s3.put_object(
            Bucket=bucket_name,
            Key=f'{uuid}.jpg',
            Body=photo['content'],
            ContentType='image/jpeg'
        )

        # DynamoDB - salvar dados
        table.put_item(Item={
            'identifier': uuid,
            'nome': nome
        })

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created'})
        }
    elif path == '/authentication':
        content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')
        
        if not content_type.startswith('multipart/form-data'):
            return {
            'statusCode': 400,
            'body': json.dumps({'message':'Content-Type inválido. Esperado: multipart/form-data'})
            }

        if not event.get("body"):
            return {
                'statusCode': 400,
                'body': json.dumps({'message':'Body inválido. Esperado: multipart/form-data'})
            }

        body = event['body']
        if event.get("isBase64Encoded"):
            body = base64.b64decode(body)

        multipart_data = decoder.MultipartDecoder(body, content_type)

        form_data = {}
        for part in multipart_data.parts:
            content_disposition = part.headers[b'Content-Disposition'].decode()
            name = content_disposition.split("name=")[1].split(";")[0].replace('"', '')
            if b'filename' in part.headers[b'Content-Disposition']:
                form_data['photo'] = {
                    'filename': part.headers[b'Content-Disposition'].decode().split('filename=')[1].replace('"', '').strip(),
                    'content': part.content
                }
            else:
                form_data[name] = part.text

        nome = form_data.get('nome')
        print(f'Nome: {nome}')
        photo = form_data.get('photo')
        print(f'Photo: {photo}')
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User authenticated'})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Not found'})
        }

#decimal utils
def decimal_default(obj):
    if isinstance(obj, Decimal):
        try:
            return int(obj) 
        except (ValueError, OverflowError):
            return float(obj) 
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
