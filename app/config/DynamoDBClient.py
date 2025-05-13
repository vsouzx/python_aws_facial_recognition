import boto3

class DynamoDBClient:
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        
    def get_connection(self, tableName: str):
        return self.dynamodb.Table(tableName)
    
    