import json
import boto3
import os
import base64
from app.repository.users_repository import find_by_identifier, save_item
from datetime import datetime

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

try:
    bucket_name = os.environ['BUCKET_NAME']
    collection_id = os.environ['COLLECTION_ID']
except KeyError:
    raise EnvironmentError("The environment variable is not configured.")

def authenticate(event):
    try:
        data = json.loads(event['body'])
        photo_base64 = data.get('photo')
        
        if not all([photo_base64]):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Required fields: photo'})
            }
            
        photo_bytes = validate_base64(photo_base64)
        
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
            
        # Buscar rosto na coleção
        response = rekognition.search_faces_by_image(
            CollectionId=collection_id,
            Image={'Bytes': photo_bytes},
            FaceMatchThreshold=90,
            MaxFaces=1
        )
        
        matches = response.get('FaceMatches', [])
        if not matches:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Nenhum rosto correspondente encontrado.'})
            }

        match = matches[0]
        identifier = match['Face']['ExternalImageId']
        confidence = match['Similarity']

        # Buscar no DynamoDB
        result = find_by_identifier(identifier)
        user = result.get('Item')

        if not user:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Usuário não encontrado no dynamodb'})
            }

        # Atualizar quantidade de acessos e última data
        user['access_count'] = user.get('access_count', 0) + 1
        user['last_access'] = str(datetime.now())

        save_item(user)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'identifier': identifier,
                'name': user['name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'access_count': user['access_count'],
                'confidence': confidence
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Erro while authenticating user: {e}'})
        }
  
def validate_base64(photo_base64):
    if ',' in photo_base64:
        photo_base64 = photo_base64.split(',')[1]

    try:
        return base64.b64decode(photo_base64)
    except Exception as e:
        print(f'Erro ao validar base64 {e}')
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid base64.'})
        }

def is_face(photo_bytes):
    response = rekognition.detect_faces(
        Image={'Bytes': photo_bytes},
        Attributes=['ALL']
    )
    
    print(f'Response deteccao face: {response}')
    faces = response.get('FaceDetails', [])

    print(f'Faces: {response}')
    if not faces:
        return False

    if len(faces) > 1:
        raise Exception('MultipleFacesException')

    return faces[0]['Confidence'] > 90