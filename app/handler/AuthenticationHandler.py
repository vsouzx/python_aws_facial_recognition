from app.handler import HandlerStrategy
from app.service import AuthenticationService

class AuthenticationHandler(HandlerStrategy):
    
    def __init__(self, authentication_service: AuthenticationService):
        super().__init__()
        self.authentication_service = authentication_service
    
    def handle(self, event):
        return self.authentication_service(event)
             