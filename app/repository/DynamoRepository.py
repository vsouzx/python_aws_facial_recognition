from app.config import DynamoDBClient

class DynamoRepository:
    
    def __init__(self, dynamoDB: DynamoDBClient, tableName: str):
        self.table = dynamoDB.get_connection(tableName)

    def saveItem(self, item: object):
        self.table.put_item(Item=item)

    def findByKey(self, key: object):
        return self.table.get_item(key)