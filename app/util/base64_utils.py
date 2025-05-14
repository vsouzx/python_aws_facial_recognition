import base64
from app.util.response_utils import ResponseUtils

class Base64Utils:
    
    def __init__(self):
        self.response_utils = ResponseUtils()

    def validate_base64(self, photo_base64: str):
        if ',' in photo_base64:
            photo_base64 = photo_base64.split(',')[1]

        try:
            return base64.b64decode(photo_base64)
        except Exception as e:
            print(f'Erro ao validar base64 {e}')
            return self.response_utils.default_response(400, f'Invalid base64: {e}')