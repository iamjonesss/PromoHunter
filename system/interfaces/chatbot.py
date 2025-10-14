from abc import ABC, abstractmethod

class ChatbotInterface(ABC):
    """Interface para integração com diferentes plataformas de chatbot.
    """
    
    def __init__(self, token: str):
        self.token = token

    @abstractmethod
    def send_message(self, chat_id: int, text: str):
        """Método responsável por fazer envio de mensagens em determinada aplicação da qual for usada.
        """
        pass

    @abstractmethod
    def receive_message(self):
        """ Método responsável por fazer recebimento de mensagens em determinada aplicação da qual for usada.
        """
        pass
