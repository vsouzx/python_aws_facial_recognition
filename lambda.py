from app.handler import HandlerMap

def lambda_handler(event, context):
    print(f'Event: {event}')
    path = event['path']
    method = event["httpMethod"]
    
    return {
            "statusCode": 200,
            "body": f"Rota {method} {path} não encontrada",
            "headers":{
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            }
        }


    #strategy = HandlerMap.getHandlerMap().get((method, path))

    #if strategy:
    #    return strategy.handle(event)
    #else:
    #    return {
    #        "statusCode": 404,
    #        "body": f"Rota {method} {path} não encontrada"
    #    }