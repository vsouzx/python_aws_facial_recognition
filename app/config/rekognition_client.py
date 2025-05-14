import boto3

class BucketS3Client:
    
    def __init__(self):
        print('dentro cosntrutor s3 client')
        self.client = boto3.client('s3')
        
