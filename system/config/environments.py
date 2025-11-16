from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Environments(BaseSettings):
    """
    Classe de configuração centralizada para o PromoHunter.
    """
    TELEGRAM_TOKEN: SecretStr

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding='utf-8',
        extra='ignore'
    )
