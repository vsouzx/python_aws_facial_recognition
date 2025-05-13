import uuid
import json
import os
from datetime import datetime
from app.config import BucketS3Client, RekognitionClient, DynamoDBClient
from app.repository.DynamoRepository import DynamoRepository
from app.util import ResponseUtils, Base64Utils, RekognitionUtils
from botocore.exceptions import ClientError

class RegisterService:
    
    def __init__(self, s3_client: BucketS3Client, 
                 rekognition_client: RekognitionClient,
                 dynamodb_client: DynamoDBClient,
                 response_utils: ResponseUtils,
                 base64_utils: Base64Utils,
                 rekognition_utils: RekognitionUtils):
        self.s3_client = s3_client.get_client()
        self.rekognition = rekognition_client.get_client()
        self.repository = DynamoRepository(dynamodb_client, os.environ["DYNAMODB_TABLE"])
        self.response_utils = response_utils
        self.base64_utils = base64_utils
        self.rekognition_utils = rekognition_utils
        self.bucket_name = os.environ['BUCKET_NAME']
        self.collection_id = os.environ['COLLECTION_ID']

    def registerNewUser(self, event):
        try:
            data = json.loads(event['body'])
    
            name = data.get('name')
            last_name = data.get('last_name')
            email = data.get('email')
            photo_base64 = data.get('photo')

            if not all([name, last_name, email, photo_base64]):
                return self.response_utils.default_response(400, 'Required fields: name, last_name, email and photo')

            photo_bytes = self.base64_utils.validate_base64(photo_base64)

            try:
                is_human_face = self.rekognition_utils.is_face(photo_bytes)
            except Exception as e:
                if str(e) == "MultipleFacesException":
                    return self.response_utils.default_response(400, 'More than one face detected.')
                return self.response_utils.default_response(400, f'Error in face detection: {e}')

            if not is_human_face:
                return self.response_utils.default_response(400, 'No human face detected or confidence too low.')
            
            identifier = str(uuid.uuid4())

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=identifier,
                Body=photo_bytes,
                ContentType='image/png'
            )

            self.create_collection_if_not_exists()
                
            self.index_faces(identifier)
            
            self.repository.save_item({
                'identifier': identifier,
                'name': name,
                'last_name': last_name,
                'email': email,
                'last_access': str(datetime.now()),
                'access_count': 0
            })

            return self.response_utils.no_content_response()
        except Exception as e:
            return self.response_utils.default_response(500, f'Erro while saving new user: {e}')

    def index_faces(self, identifier: str):
        try:
            self.rekognition.index_faces(
                CollectionId=self.collection_id,
                Image={
                    'S3Object': {
                        'Bucket': self.bucket_name,
                        'Name': identifier
                    }
                },
                ExternalImageId=identifier,
                DetectionAttributes=['ALL']
            )
        except Exception as e:
            return self.response_utils.default_response(500, f'Error indexing face: {e}')
              
    def create_collection_if_not_exists(self):
        try:
            self.rekognition.create_collection(CollectionId=self.collection_id)
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                return self.response_utils.default_response(500, f'Error creating collection: {e}')