from app.handler.factory import HandlerFactory

def lambda_handler(event, context):
    print(f'Event: {event}')
    path = event['path']
    method = event["httpMethod"]
    
    handler = HandlerFactory()
    
    strategy = handler.get((method, path))

    if strategy:
        return strategy.handle(event)
    else:
        return {
            "statusCode": 404,
            "body": f"Rota {method} {path} não encontrada"
        }