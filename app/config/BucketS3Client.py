import boto3

class BucketS3Client:
    
    def __init__(self):
        self.bucketS3 = boto3.client('s3')
        
    def get_client(self):
        return self.bucketS3