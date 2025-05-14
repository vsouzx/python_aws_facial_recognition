from app.handler import HandlerStrategy
from app.service import AuthenticationService

class AuthenticationHandler(HandlerStrategy):
    
    def __init__(self):
        super().__init__()
    
    def handle(self, event):
        return AuthenticationService.authenticate(event)
             