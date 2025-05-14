from app.service.register_service import RegisterService

class RegisterHandler:
    
    def __init__(self):
        pass

    def handle(self, event):
        return RegisterService().register_new_user(event)
    
    def description(self):
        return RegisterService().description()
             