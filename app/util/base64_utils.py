import base64
from app.util.response_utils import default_response

def validate_base64(photo_base64):
    if ',' in photo_base64:
        photo_base64 = photo_base64.split(',')[1]

    try:
        return base64.b64decode(photo_base64)
    except Exception as e:
        print(f'Erro ao validar base64 {e}')
        return default_response(400, f'Invalid base64: {e}')