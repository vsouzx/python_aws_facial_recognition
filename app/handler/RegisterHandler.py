from app.handler import HandlerStrategy
from app.service import RegisterService

class RegisterHandler(HandlerStrategy):
    
    def __init__(self, register_service: RegisterService):
        super().__init__()
        self.register_service = register_service
    
    def handle(self, event):
        return self.register_service(event)
             