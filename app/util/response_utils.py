import json

def no_content_response():
    return {
        'statusCode': 201,
        'headers': headers
    }
    
def default_response(status, message):
    return {
        'statusCode': status,
        'headers': headers(),
        'body': json.dumps({'message': message})
    }
    
def custom_response(status, body):
    return {
        'statusCode': status,
        'headers': headers(),
        'body': json.dumps(body)
    }
    
def headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,POST'
    }
    
#teste