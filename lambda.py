from app.service.register_service import register_new_user, find_user_by_image

def lambda_handler(event, context):
    print(f'Event: {event}')

    path = event['path']

    if path == '/register':
        return register_new_user(event)
    elif path == '/authentication':
        return find_user_by_image(event)