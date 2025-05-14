from app.config.RekognitionClient import RekognitionClient

class RekognitionUtils:
    
    def is_face(self, photo_bytes):
        response = RekognitionClient.detect_faces(
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

