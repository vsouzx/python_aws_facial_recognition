import uuid
import json
import boto3
import os
import base64
from app.repository.users_repository import save_item

s3 = boto3.client('s3')

try:
    bucket_name = os.environ['BUCKET_NAME']
except KeyError:
    raise EnvironmentError("A variável de ambiente não está configurada.")

def register_new_user(event):
    try:
        data = json.loads(event['body'])
    
        nome = data.get('nome')
        print(f'Nome: {nome}' )
        foto_base64 = data.get('photo')
        print(f'Base64: {foto_base64}' )

        if not all([nome, foto_base64]):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Campos obrigatórios: nome e foto_base64'})
            }

        if not all([nome, foto_base64]):
            return {
                'statusCode': 400,
                'body': json.dumps('Todos os campos são obrigatórios.')
            }
        
        # Remover prefixo se houver
        if ',' in foto_base64:
            foto_base64 = foto_base64.split(',')[1]

        try:
            foto_bytes = base64.b64decode(foto_base64)
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Base64 da imagem inválido'})
            }

        identifier = str(uuid.uuid4())

        s3.put_object(
            Bucket=bucket_name,
            Key=identifier,
            Body=foto_bytes,
            ContentType='image/png'
        )

        save_item({
            'identifier': identifier,
            'nome': nome
        })

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Erro ao salvar novo usuário: {e}'})
        }