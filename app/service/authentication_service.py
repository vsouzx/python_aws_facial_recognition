import json
import boto3
import os
from app.repository.users_repository import find_by_identifier, save_item
from datetime import datetime
from app.util.response_utils import default_response, custom_response
from app.util.base64_utils import validate_base64
from app.util.rekognition_utils import is_face

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

try:
    bucket_name = os.environ['BUCKET_NAME']
    collection_id = os.environ['COLLECTION_ID']
except KeyError:
    raise EnvironmentError('The environment variable is not configured.')

def authenticate(event):
    try:
        data = json.loads(event['body'])
        photo_base64 = data.get('photo')
        
        if not all([photo_base64]):
            return default_response(400, 'Required fields: photo')
            
        photo_bytes = validate_base64(photo_base64)
        
        try:
            is_human_face = is_face(photo_bytes)
        except Exception as e:
            if str(e) == 'MultipleFacesException':
                return default_response(400, 'More than one face detected.')
            print(f'Error in face detection: {e}')
            return default_response(400, 'Error in face detection.')

        if not is_human_face:
            return default_response(400, 'No human face detected or confidence too low.')
            
        # Buscar rosto na coleção
        response = rekognition.search_faces_by_image(
            CollectionId=collection_id,
            Image={'Bytes': photo_bytes},
            FaceMatchThreshold=90,
            MaxFaces=1
        )
        
        matches = response.get('FaceMatches', [])
        if not matches:
            return default_response(400, 'No correspondent face found.')

        match = matches[0]
        identifier = match['Face']['ExternalImageId']
        confidence = match['Similarity']

        # Buscar no DynamoDB
        result = find_by_identifier(identifier)
        user = result.get('Item')

        if not user:
            return default_response(400, 'User not found in dynamodb.')

        # Atualizar quantidade de acessos e última data
        user['access_count'] = user.get('access_count', 0) + 1
        user['last_access'] = str(datetime.now())

        save_item(user)
        
        return custom_response(201, {
                'identifier': identifier,
                'name': user['name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'access_count': user['access_count'],
                'confidence': confidence
            })
    except Exception as e:
        return default_response(500, f'Erro while authenticating user: {e}')
