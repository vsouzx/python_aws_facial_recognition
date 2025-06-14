import boto3

class RekognitionClient:
    
    def __init__(self):
        print('dentro cosntrutor s3 client')
        self.client = boto3.client('s3')
        
