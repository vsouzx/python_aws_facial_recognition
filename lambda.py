from decimal import Decimal
import json

def lambda_handler(event, context):
    print(f'Event: {event}')

    http_method = event['httpMethod']
    path = event['path']

    if http_method == 'POST':
        if path == '/register':
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'User created'})
            }
        elif path == '/authentication':
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'User authenticated'})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Path not found'})
            }
    #estive aqui
    return {
        'statusCode': 405,
        'body': json.dumps('Method not allowed')
    }

#decimal utils
def decimal_default(obj):
    if isinstance(obj, Decimal):
        try:
            return int(obj) 
        except (ValueError, OverflowError):
            return float(obj) 
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
