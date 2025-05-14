import boto3

class BucketS3Client:
    
    def __init__(self):
        print('dentro cosntrutor s3 client')
        self.bucketS3 = boto3.client('s3')
        
    def get_client(self):
        print('dentro get_clientget_client s3 client')
        return self.bucketS3