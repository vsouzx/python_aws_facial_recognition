from decimal import Decimal
import json

def lambda_handler(event, context):
    print(f'Event: {event}')

    path = event['path']

    if path == '/register':
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created'})
        }
    elif path == '/authentication':
        content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')
        
        body = event['body']
        if event.get("isBase64Encoded"):
            body = base64.b64decode(body)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User authenticated'})
        }

#decimal utils
def decimal_default(obj):
    if isinstance(obj, Decimal):
        try:
            return int(obj) 
        except (ValueError, OverflowError):
            return float(obj) 
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
