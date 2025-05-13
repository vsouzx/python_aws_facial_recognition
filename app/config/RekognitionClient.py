import boto3

class RekognitionClient:
    
    def __init__(self):
        self.rekognition = boto3.client('rekognition')
        
    def get_client(self):
        return self.rekognition