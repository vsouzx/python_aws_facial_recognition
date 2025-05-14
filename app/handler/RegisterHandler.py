from app.handler import HandlerStrategy
from app.service import RegisterService

class RegisterHandler(HandlerStrategy):
    
    def __init__(self):
        super()
    
    def handle(self, event):
        return RegisterService.registerNewUser(event)
             