import uuid
import json
import boto3
import os
import base64
from app.repository.users_repository import save_item
from datetime import datetime
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

try:
    bucket_name = os.environ['BUCKET_NAME']
    collection_id = os.environ['COLLECTION_ID']
except KeyError:
    raise EnvironmentError("The environment variable is not configured.")

def register_new_user(event):
    try:
        data = json.loads(event['body'])
    
        name = data.get('name')
        print(f'Name: {name}' )
        last_name = data.get('last_name')
        print(f'Last name: {last_name}' )
        email = data.get('email')
        print(f'Email: {email}' )
        photo_base64 = data.get('photo')

        if not all([name, last_name, email, photo_base64]):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Required fields: name, last_name, email and photo'})
            }

        # Remover prefixo se houver
        if ',' in photo_base64:
            photo_base64 = photo_base64.split(',')[1]

        try:
            photo_bytes = base64.b64decode(photo_base64)
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid base64.'})
            }

        try:
            is_human_face = is_face(photo_bytes)
        except Exception as e:
            if str(e) == "MultipleFacesException":
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'More than one face detected.'})
                }
            print(f'Error in face detection: {e}')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Error in face detection.'})
            }

        if not is_human_face:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'No human face detected or confidence too low.'})
            }
            
        identifier = str(uuid.uuid4())

        s3.put_object(
            Bucket=bucket_name,
            Key=identifier,
            Body=photo_bytes,
            ContentType='image/png'
        )

        # Criar coleção, se não existir
        try:
            rekognition.create_collection(CollectionId=collection_id)
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                return {
                    'statusCode': 500,
                    'body': json.dumps({'message': f'Error creating collection: {e}'})
                }
                
         # Indexar o rosto na coleção
        try:
            rekognition.index_faces(
                CollectionId=collection_id,
                Image={
                    'S3Object': {
                        'Bucket': bucket_name,
                        'Name': identifier
                    }
                },
                ExternalImageId=identifier,
                DetectionAttributes=['ALL']
            )
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': f'Error indexing face: {e}'})
            }
            
        save_item({
            'identifier': identifier,
            'name': name,
            'last_name': last_name,
            'email': email,
            'last_access': str(datetime.now()),
            'access_count': 0
        })

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Erro while saving new user: {e}'})
        }
        
def find_user_by_image(event):
    return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User authenticated'})
        }
    
def is_face(photo_bytes):
    print('iniciando deteccao face')
    try:
        response = rekognition.detect_faces(
        Image={'Bytes': photo_bytes},
        Attributes=['ALL']
    )
    except Exception as e:
        print(f'Erro ao detectar faceeeeeeeeee {e}')
    
    print(f'Response deteccao face: {response}')
    faces = response.get('FaceDetails', [])

    print(f'Faces: {response}')
    if not faces:
        return False

    if len(faces) > 1:
        raise Exception('MultipleFacesException')

    return faces[0]['Confidence'] > 90