from app.service.authentication_service import AuthenticationService

class AuthenticationHandler:

    def __init__(self):
        pass
        
    def handle(self, event):
        return AuthenticationService().authenticate(event)
    
    def description(self):
        return AuthenticationService().description()