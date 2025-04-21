import uuid
import json
import boto3
import os
from app.repository.users_repository import save_item
from datetime import datetime
from botocore.exceptions import ClientError
from app.util.response_utils import no_content_response, default_response
from app.util.base64_utils import validate_base64
from app.util.rekognition_utils import is_face

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
            return default_response(400, 'Required fields: name, last_name, email and photo')

        photo_bytes = validate_base64(photo_base64)

        try:
            is_human_face = is_face(photo_bytes)
        except Exception as e:
            if str(e) == "MultipleFacesException":
                return default_response(400, 'More than one face detected.')
            return default_response(400, f'Error in face detection: {e}')

        if not is_human_face:
            return default_response(400, 'No human face detected or confidence too low.')
            
        identifier = str(uuid.uuid4())

        s3.put_object(
            Bucket=bucket_name,
            Key=identifier,
            Body=photo_bytes,
            ContentType='image/png'
        )

        create_collection_if_not_exists()
                
        index_faces(identifier)
            
        save_item({
            'identifier': identifier,
            'name': name,
            'last_name': last_name,
            'email': email,
            'last_access': str(datetime.now()),
            'access_count': 0
        })

        return no_content_response()
    except Exception as e:
        return default_response(500, f'Erro while saving new user: {e}')
  
def index_faces(identifier):
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
        return default_response(500, f'Error indexing face: {e}')
              
def create_collection_if_not_exists():
    try:
        rekognition.create_collection(CollectionId=collection_id)
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
            return default_response(500, f'Error creating collection: {e}')