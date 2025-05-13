from abc import ABC, abstractmethod

class HandlerStrategy(ABC):
    
    @abstractmethod
    def handle(self, event):
        pass