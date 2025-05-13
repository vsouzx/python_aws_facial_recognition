from app.handler import RegisterHandler, AuthenticationHandler

class HandlerMap:
    
    def __init__(self):
        pass
    
    def getHandlerMap(self):
        return {
            ("POST", "/authentication"): AuthenticationHandler(),
            ("POST", "/register"): RegisterHandler()
        }