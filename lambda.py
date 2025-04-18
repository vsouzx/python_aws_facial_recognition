from app.service.register_service import register_new_user
from app.service.authentication_service import authenticate

def lambda_handler(event, context):
    print(f'Event: {event}')

    path = event['path']

    if path == '/register':
        return register_new_user(event)
    elif path == '/authentication':
        return authenticate(event)