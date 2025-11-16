import logging
import sys

class BotLogger:
    """
    Uma classe para configurar e fornecer um logger centralizado.
    """
    def __init__(self, nome_logger: str, nivel_log=logging.INFO):
        """
        Inicializa e configura o logger.

        Args:
            nome_logger (str): O nome do logger (geralmente __name__ do módulo que o utiliza).
            nivel_log: O nível de log a ser capturado (ex: logging.INFO, logging.DEBUG).
        """
        self.logger = logging.getLogger(nome_logger)
        self.logger.setLevel(nivel_log)

        if not self.logger.handlers:
            handler_console = logging.StreamHandler(sys.stdout)

            formato_log = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            handler_console.setFormatter(formato_log)

            self.logger.addHandler(handler_console)

    def get_logger(self) -> logging.Logger:
        """
        Retorna a instância configurada do logger.

        Returns:
            logging.Logger: O objeto logger.
        """
        return self.logger
