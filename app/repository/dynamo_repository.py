from app.config.dynamo_db_client import DynamoDBClient

class DynamoRepository:
    
    def __init__(self, tableName: str):
        self.table = DynamoDBClient().get_connection(tableName)

    def saveItem(self, item: object):
        self.table.put_item(Item=item)

    def findByKey(self, key: object):
        return self.table.get_item(key)