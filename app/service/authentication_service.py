import json
import os
from datetime import datetime
from app.config.buckets3_client import BucketS3Client
from app.config.rekognition_client import RekognitionClient
from app.repository.dynamo_repository import DynamoRepository
from app.util.response_utils import ResponseUtils
from app.util.base64_utils import Base64Utils
from app.util.rekognition_utils import RekognitionUtils

class AuthenticationService:
    
    def __init__(self):
        self.user_repository = DynamoRepository(os.environ['DYNAMODB_TABLE'])
        self.response_utils = ResponseUtils()
        self.base64_utils = Base64Utils()
        self.rekognition_utils = RekognitionUtils()
        self.bucket_name = os.environ['BUCKET_NAME']
        self.collection_id = os.environ['COLLECTION_ID']

    def authenticate(self, event):
        try:
            data = json.loads(event['body'])
            photo_base64 = data.get('photo')
        
            if not all([photo_base64]):
                return self.response_utils.default_response(400, 'Required fields: photo')
            
            photo_bytes = self.base64_utils.validate_base64(photo_base64)
        
            try:
                is_human_face = self.rekognition_utils.is_face(photo_bytes)
            except Exception as e:
                if str(e) == 'MultipleFacesException':
                    return self.response_utils.default_response(400, 'More than one face detected.')
                print(f'Error in face detection: {e}')
                return self.response_utils.default_response(400, 'Error in face detection.')

            if not is_human_face:
                return self.response_utils.default_response(400, 'No human face detected or confidence too low.')
            
            response = self.RekognitionClient().client.search_faces_by_image(
                CollectionId=self.collection_id,
                Image={'Bytes': photo_bytes},
                FaceMatchThreshold=90,
                MaxFaces=1
            )
        
            matches = response.get('FaceMatches', [])
            if not matches:
                return self.response_utils.default_response(400, 'No correspondent face found.')

            match = matches[0]
            identifier = match['Face']['ExternalImageId']
            confidence = match['Similarity']

            result = self.user_repository.findByKey(Key={'identifier': identifier})
            user = result.get('Item')

            if not user:
                return self.response_utils.default_response(400, 'User not found in dynamodb.')

            user['access_count'] = user.get('access_count', 0) + 1
            user['last_access'] = str(datetime.now())

            self.user_repository.save_item(user)
        
            return self.response_utils.custom_response(201, {
                    'identifier': identifier,
                    'name': user['name'],
                    'last_name': user['last_name'],
                    'email': user['email'],
                    'access_count': user['access_count'],
                    'confidence': confidence
                }
            )
        except Exception as e:
            return self.response_utils.default_response(500, f'Erro while authenticating user: {e}')

    def description(self):
        return "register_service"