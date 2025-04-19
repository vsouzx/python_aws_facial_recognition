from requests_toolbelt.multipart import decoder
from decimal import Decimal
from app.service.register_service import register_new_user


def lambda_handler(event, context):
    print(f'Event: {event}')

    path = event['path']

    if path == '/register':
        return register_new_user(event)
    elif path == '/authentication':
        content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')
        
        if not content_type.startswith('multipart/form-data'):
            return {
            'statusCode': 400,
            'body': json.dumps({'message':'Content-Type inválido. Esperado: multipart/form-data'})
            }

        if not event.get("body"):
            return {
                'statusCode': 400,
                'body': json.dumps({'message':'Body inválido. Esperado: multipart/form-data'})
            }

        body = event['body']
        if event.get("isBase64Encoded"):
            body = base64.b64decode(body)

        multipart_data = decoder.MultipartDecoder(body, content_type)

        form_data = {}
        for part in multipart_data.parts:
            content_disposition = part.headers[b'Content-Disposition'].decode()
            name = content_disposition.split("name=")[1].split(";")[0].replace('"', '')
            if b'filename' in part.headers[b'Content-Disposition']:
                form_data['photo'] = {
                    'filename': part.headers[b'Content-Disposition'].decode().split('filename=')[1].replace('"', '').strip(),
                    'content': part.content
                }
            else:
                form_data[name] = part.text

        nome = form_data.get('nome')
        print(f'Nome: {nome}')
        photo = form_data.get('photo')
        print(f'Photo: {photo}')
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User authenticated'})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Not found'})
        }

#decimal utils
def decimal_default(obj):
    if isinstance(obj, Decimal):
        try:
            return int(obj) 
        except (ValueError, OverflowError):
            return float(obj) 
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
