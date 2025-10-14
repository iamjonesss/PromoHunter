"""
Arquivo de configuração para o PromoHunter.

Este módulo centraliza as configurações da aplicação, incluindo variáveis de ambiente,
configurações de API e parâmetros do sistema.
"""

import os
from typing import Optional
from .logger import BotLogger

class Config:
    """Classe de configuração centralizada para o PromoHunter."""
    
    def __init__(self):
        self.logger = BotLogger(__name__).get_logger()
        self._load_config()
    
    def _load_config(self):
        """Carrega as configurações do ambiente."""
        self.logger.info("Loading application configuration...")
        
        # Configurações do Telegram
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.TELEGRAM_WEBHOOK_URL = os.getenv('TELEGRAM_WEBHOOK_URL')
        
        # Configurações da aplicação
        self.APP_NAME = "PromoHunter"
        self.APP_VERSION = "1.0.0"
        self.DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
        
        # Configurações de logging
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
        self.LOG_FILE = os.getenv('LOG_FILE', 'promohunter.log')
        
        # Configurações de API (para futuras integrações)
        self.API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
        self.MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
        
        # Validar configurações obrigatórias
        self._validate_config()
    
    def _validate_config(self):
        """Valida se as configurações obrigatórias estão presentes."""
        if not self.TELEGRAM_TOKEN:
            self.logger.warning("TELEGRAM_TOKEN not configured")
    
    def get_telegram_token(self) -> Optional[str]:
        """Retorna o token do Telegram.
        
        Returns:
            Optional[str]: Token do Telegram ou None se não configurado
        """
        return self.TELEGRAM_TOKEN
    
    def is_debug_enabled(self) -> bool:
        """Verifica se o modo debug está ativado.
        
        Returns:
            bool: True se debug está ativo, False caso contrário
        """
        return self.DEBUG_MODE
    
    def get_app_info(self) -> dict:
        """Retorna informações da aplicação.
        
        Returns:
            dict: Dicionário com informações da aplicação
        """
        return {
            'name': self.APP_NAME,
            'version': self.APP_VERSION,
            'debug': self.DEBUG_MODE
        }
    
    def __str__(self) -> str:
        """Representação string das configurações (sem informações sensíveis)."""
        return (
            f"Config(app={self.APP_NAME} v{self.APP_VERSION}, "
            f"debug={self.DEBUG_MODE}, "
            f"telegram_configured={bool(self.TELEGRAM_TOKEN)})"
        )

# Instância global de configuração
config = Config()