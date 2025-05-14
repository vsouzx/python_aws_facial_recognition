from app.handler.register_handler import RegisterHandler
from app.handler.authentication_handler import AuthenticationHandler

class HandlerFactory:
    
    def __init__(self):
        pass
    
    def get(self, key):
        return self.set_strategies().get(key, None)
    
    def set_strategies(self):
        return {
            ("POST", "/authentication"): AuthenticationHandler(),
            ("POST", "/register"): RegisterHandler()
        }
    