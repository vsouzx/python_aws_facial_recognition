import json
from app.util.decimal_utils import DecimalUtils

class ResponseUtils:

    def __init__(self):
        self.decimal_utils = DecimalUtils()

    def no_content_response(self):
        return {
            'statusCode': 201,
            'headers': self.headers()
        }
    
    def default_response(self, status: int, message: str):
        return {
            'statusCode': status,
            'headers': self.headers(),
            'body': json.dumps({'message': message})
        }
    
    def custom_response(self, status: int, body: object):
        return {
            'statusCode': status,
            'headers': self.headers(),
            'body': json.dumps(body, default=self.decimal_utils.decimal_default)
        }
    
    def headers():
        return {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        }