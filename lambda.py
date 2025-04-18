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
        # content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')
        
        # if not content_type.startswith('multipart/form-data'):
        #     return {
        #         'statusCode': 400,
        #         'body': json.dumps({'message': 'Content-Type inválido. Esperado: multipart/form-data'})
        #     }
        
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
