from config.logger import BotLogger

class CentralConfig:
    """
    Classe para configurar e fornecer acesso centralizado ao logger.
    """
    def __init__(self):
        """
        Inicializa a configuração central e o logger.
        """
        self.logger = BotLogger(__name__).get_logger()

    def get_logger(self):
        """
        Retorna o logger configurado.

        Returns:
            logging.Logger: O objeto logger.
        """
        return self.log
