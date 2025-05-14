from app.config.rekognition_client import RekognitionClient

class RekognitionUtils:
    
    def __init__(self):
        self.rekognition_client = RekognitionClient().get_client()

    def is_face(self, photo_bytes):
        response = self.rekognition_client.detect_faces(
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

