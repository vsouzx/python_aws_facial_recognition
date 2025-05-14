import uuid
import json
import os
from datetime import datetime
from app.config.buckets3_client import BucketS3Client
from app.config.rekognition_client import RekognitionClient
from app.repository.dynamo_repository import DynamoRepository
from app.util.response_utils import ResponseUtils
from app.util.base64_utils import Base64Utils
from app.util.rekognition_utils import RekognitionUtils
from botocore.exceptions import ClientError

class RegisterService:
    
    def __init__(self):
        print('dentro do construtor')
        try:
            self.repository = DynamoRepository(os.environ["DYNAMODB_TABLE"])
            self.response_utils = ResponseUtils()
            self.base64_utils = Base64Utils()
            self.rekognition_utils = RekognitionUtils()
            self.bucket_name = os.environ['BUCKET_NAME']
            self.collection_id = os.environ['COLLECTION_ID']
        except Exception as e:
            print(f'Erro durante init: {e}')
            raise e  # opcional: relança o erro para não mascarar problemas

    def register_new_user(self, event):
        print('dentro do register_new_user')
        try:
            data = json.loads(event['body'])
    
            name = data.get('name')
            last_name = data.get('last_name')
            email = data.get('email')
            photo_base64 = data.get('photo')

            print(f'params: {name}, {last_name}, {email}, {photo_base64}')

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

            self.BucketS3Client().client.put_object(
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
            self.RekognitionClient().clientRekognition.index_faces(
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
            self.RekognitionClient().clientRekognition.create_collection(CollectionId=self.collection_id)
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                return self.response_utils.default_response(500, f'Error creating collection: {e}')

    def description(self):
        return "register_service"