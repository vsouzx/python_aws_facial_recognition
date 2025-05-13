from app.handler import HandlerMap

def lambda_handler(event, context):
    print(f'Event: {event}')
    path = event['path']
    method = event["httpMethod"]

    strategy = HandlerMap.getHandlerMap().get((method, path))

    if strategy:
        return strategy.handle(event)
    else:
        return {
            "statusCode": 404,
            "body": f"Rota {method} {path} não encontrada"
        }